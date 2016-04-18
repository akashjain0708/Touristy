import json
import uuid
from werkzeug.security import generate_password_hash

from database_interaction import *
import flask_login as flask_login
from recommender import *
from flask_login import login_required, logout_user, login_user, current_user
from User import *
from flask import Flask, request, render_template, make_response, url_for, redirect

app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return make_response(render_template('index.html'))


@app.route('/loginUser', methods=['POST'])
def login_user_id():
    login_json = json.loads(request.get_json())
    user_id = login_json["userID"]
    password = login_json["password"]
    result = login_user_database(user_id, password)
    if result[0] == "OK":
        login_user(user_id)
    return result


@app.route('/createUser', methods=['POST'])
def create_user_by_id():
    user_json = json.loads(request.get_json())
    print("Creating user")
    user_id = user_json["UserName"]
    name = user_json["FullName"]
    email_id = user_json["EmailID"]
    phone_no = user_json["PhoneNumber"]
    password = user_json["Password"]
    hashed_password = generate_password_hash(password)
    result = add_user(user_id, name, email_id, phone_no, hashed_password)
    return result


def get_posts_for_locations(recommend_location_list):
    recommend_list = []
    # For every location, take the top most post, and create a list
    for location in recommend_location_list:
        recommended_post = select_lat_long(location[0], location[1])[0]
        item_json = {"LocationName": recommended_post[4],
                     "Time": recommended_post[5],
                     "Price": recommended_post[6],
                     "Rating": recommended_post[7],
                     "UserName": recommended_post[3],
                     "Description": recommended_post[2],
                     "UpVotes": recommended_post[0],
                     "DownVotes": recommended_post[1],
                     "PostID": recommended_post[8]
                     }
        recommend_list.append(item_json)
    return recommend_list


@app.route('/search', methods=['POST'])
def search_place():
    print("Hey there")
    query_json = request.get_json()
    print(query_json["LocationName"])
    latitude = query_json["Latitude"]
    longitude = query_json["Longitude"]
    tag_list = query_json["Tags"]
    results_list = select_lat_long(latitude, longitude)
    display_list = []
    # Makes posts for search results
    for result in results_list:
        item_json = {"LocationName": result[4],
                     "Time": result[5],
                     "Price": result[6],
                     "Rating": result[7],
                     "UserName": result[3],
                     "Description": result[2],
                     "UpVotes": result[0],
                     "DownVotes": result[1],
                     "PostID": result[8]
                     }
        display_list.append(item_json)

    # Add to recommendation list
    insert_recommend_location(tag_list, (latitude, longitude))
    # Gets list of recommended locations with location data
    recommend_location_list = new_click_recommendation((latitude, longitude))
    # Create posts for recommendation
    recommend_list = get_posts_for_locations(recommend_location_list)
    return json.dumps(display_list, recommend_list)

UNDEFINED = 'null'


@app.route('/search', methods=['POST'])
def search_place_filters():
    print("Hey there")
    query_json = request.get_json()
    print(query_json["LocationName"])
    latitude = query_json["Latitude"]
    longitude = query_json["Longitude"]
    time = query_json["Time"]
    cost = query_json["Cost"]
    rating = query_json["Rating"]

    if time == UNDEFINED and cost == UNDEFINED and rating == UNDEFINED:
        results_list = select_lat_long(latitude, longitude)

    elif time == UNDEFINED and cost == UNDEFINED:
        results_list = select_lat_long_rating(latitude, longitude, rating)

    elif time == UNDEFINED and rating == UNDEFINED:
        results_list = select_lat_long_cost(latitude, longitude, cost)

    elif time == UNDEFINED:
        results_list = select_lat_long_cost_rating(latitude, longitude, cost, rating)

    elif cost == UNDEFINED and rating == UNDEFINED:
        results_list = select_lat_long_time(latitude, longitude, time)

    elif cost == UNDEFINED:
        results_list = select_lat_long_time_rating(latitude, longitude, time, rating)

    elif rating == UNDEFINED:
        results_list = select_lat_long_time_cost(latitude, longitude, time, cost)

    else:
        results_list = select_lat_long_time_cost_rating(latitude, longitude, time, cost, rating)

    return_list = []
    for result in results_list:
        item_json = {"LocationName": result[4],
                     "Time": result[5],
                     "Price": result[6],
                     "Rating": result[7],
                     "UserName": result[3],
                     "Description": result[2],
                     "UpVotes": result[0],
                     "DownVotes": result[1],
                     "PostID":result[8]
                     }
        return_list.append(item_json)
    print(return_list)
    print(json.dumps(return_list))
    return json.dumps(return_list)


@app.route('/myPosts')
@login_required
def user_posts():
    user_id = current_user.get_id()
    my_posts = get_user_posts(user_id)
    return json.dumps(my_posts)


@app.route('/createPost', methods=['POST'])
@login_required
def make_post_for_user():
    print("Creating a post")
    post_json = request.get_json()
    print(post_json)

    # TODO: Get user name from frontend, and generate postID
    user_id = current_user.get_id()
    post_id = uuid.uuid4()
    description = post_json["Description"]
    upvotes = 0
    downvotes = 0
    latitude = post_json["Latitude"]
    longitude = post_json["Longitude"]
    name = post_json["LocationName"]
    time = int(post_json["Time"])
    cost = int(post_json["Price"])
    rating = int(post_json["Rating"])
    tag_list = post_json["Tags"]
    attractionid = uuid.uuid4()
    print("Sending post")
    result = add_post(post_id, upvotes, downvotes, description, user_id)
    print("Created post")
    print("Sending attraction")
    result1 = add_attraction(attractionid, latitude, longitude, name, time, cost, rating, post_id)
    insert_recommend_location(tag_list, (latitude, longitude))
    print("Created attraction")
    return result


@app.route('/deletePost', methods=['POST'])
@login_required
def delete_post_by_id():
    delete_json = request.get_json()
    print(delete_json)
    post_id = delete_json["PostID"]
    # attractionid = delete_json["attractionid"]
    print(post_id)
    remove_post(post_id)
    return "Success"


@app.route('/editPost', methods=['POST'])
@login_required
def edit_post_by_id():
    edit_json = request.get_json()
    print(edit_json)
    print("Editing post")
    post_id = edit_json["PostID"]
    description = edit_json["Description"]
    time = int(edit_json["Time"])
    cost = int(edit_json["Price"])
    rating = int(edit_json["Rating"])
    edit_ps_obj = {
        'PostID': post_id,
        'Description': description,
    }
    edit_at_obj = {
        'Time': time,
        'Cost': cost,
        'PostID': post_id,
        'Rating': rating,
    }
    edit_post(edit_ps_obj, post_id)
    print("Post edited")
    edit_attraction(edit_at_obj, post_id)
    print("Attraction edited")
    return "Success"


@app.route("/logoutUser")
@login_required
def logout():
    """
    Method to logout user
    :return:
    """
    logout_user()
    return redirect(url_for('main'))


# Generate a random secret key for Flask-Login
app.secret_key = os.urandom(24)

if __name__ == '__main__':
    app.run()
