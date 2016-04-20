import json
import uuid
from werkzeug.security import generate_password_hash

import flask_login as flask_login
from recommender import *
from flask_login import login_required, logout_user, login_user, current_user
from flask import Flask, request, render_template, make_response, url_for, redirect
from database_interaction import *
app = Flask(__name__)
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@app.route('/')
def hello_world():
    return make_response(render_template('index.html'))


@app.route('/loginUser', methods=['POST'])
def login_user_id():
    print("Hey")
    login_json = request.get_json()
    print("Hey")
    user_id = login_json["UserName"]
    print("Hey")
    password = login_json["Password"]
    print("Password:" +password)
    result = login_user_database(user_id, password)
    print("Hey")
    if result[0] == "OK":
        user_obj = User(user_id)
        print("Inside")
        login_user(user_obj)
        print("Logged in")
        print(current_user.get_id())
    print("Returning")
    print("Current User after login:" +current_user.get_id())
    return json.dumps(result)


@app.route('/signup', methods=['POST'])
def create_user_by_id():
    user_json = request.get_json()
    print(user_json)
    print("Creating user")
    if user_json.get("UserName") is None:
        return ["Error", "User name not found!"]
    if user_json.get("FullName") is None:
        return ["Error", "Full name not found!"]
    if user_json.get("Password") is None:
        return ["Error", "Password not found!"]
    if user_json.get("EmailID") is None:
        return ["Error", "Email not found!"]
    if user_json.get("PhoneNumber") is None:
        phone_no = ""
    else:
        phone_no = user_json["PhoneNumber"]
    print("Hey")
    user_id = user_json["UserName"]
    name = user_json["FullName"]
    email_id = user_json["EmailID"]
    password = user_json["Password"]
    hashed_password = generate_password_hash(password)
    result = add_user(user_id, name, email_id, phone_no, hashed_password, 0)
    if result[0] == "OK":
        user_obj = User(user_id)
        login_user(user_obj)
    return json.dumps(result)


def get_posts_for_locations(recommend_location_list):
    recommend_list = []
    print("Making recommend list")
    # For every location, take the top most post, and create a list
    for location in recommend_location_list:
        print(type(location[0]))
        posts = select_lat_long(float(location[0]), float(location[1]))
        if len(posts) is 0:
            print("Length of posts is 0")
            continue
        recommended_post = posts[0]
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
    print("Sending list")
    return recommend_list


@app.route('/search', methods=['POST'])
def search_place():
    print("Searching!")
    query_json = request.get_json()
    print(query_json["LocationName"])
    latitude = query_json["Latitude"]
    longitude = query_json["Longitude"]
    tag_list = query_json["Tags"]
    print("Tag list:" + str(tag_list))
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

    # # Add to recommendation list
    insert_recommend_location(tag_list, (latitude, longitude))
    # Gets list of recommended locations with location data
    print("Printing LatLon: ")
    print(type(latitude), type(longitude))
    recommend_location_list = new_click_recommendation((latitude, longitude))
    # Create posts for recommendation
    print("Getting posts for locations")
    recommend_list = get_posts_for_locations(recommend_location_list)
    print("Display list: " +json.dumps(display_list))
    print("Recommendation list: " +json.dumps(recommend_list))
    print("Returning")
    print(json.dumps(display_list))
    return json.dumps([display_list, recommend_list])
    # ), recommend  = json.dumps(recommend_list)


@app.route('/heatMapData', methods=['POST'])
def heat_map_data():
    print("Getting to heatmap")
    heat_json = request.get_json()
    latitude = heat_json["Latitude"]
    longitude = heat_json["Longitude"]
    print("Latitude/Longitude:" +str(latitude), str(longitude))
    result = heatmap(latitude, longitude)
    return json.dumps(result)


@app.route('/search/filters', methods=['POST'])
def search_place_filters():
    print("Hey there")
    query_json = request.get_json()
    print("Search filter json:" +str(query_json))
    print(query_json["LocationName"])
    latitude = query_json["Latitude"]
    longitude = query_json["Longitude"]

    if query_json.get("Time") is None:
        time = None
    else:
        time = query_json["Time"]
        print("Time:" +time)

    if query_json.get("Price") is None:
        cost = None
    else:
        cost = query_json["Price"]
        print("Cost:" +cost)

    if query_json.get("Rating") is None:
        rating = None
    else:
        rating = query_json["Rating"]
        print("Rating:" +rating)

    if time is None and cost is None and rating is None:
        results_list = select_lat_long(latitude, longitude)

    elif time is None and cost is None:
        results_list = select_lat_long_rating(latitude, longitude, rating)

    elif time is None and rating is None:
        results_list = select_lat_long_cost(latitude, longitude, cost)

    elif time is None:
        results_list = select_lat_long_cost_rating(latitude, longitude, cost, rating)

    elif cost is None and rating is None:
        results_list = select_lat_long_time(latitude, longitude, time)

    elif cost is None:
        results_list = select_lat_long_time_rating(latitude, longitude, time, rating)

    elif rating is None:
        print("time Cost")
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


@app.route('/myPosts', methods=['POST'])
def user_posts():
    print("My posts")
    user_id = request.get_json()["UserID"]
    print("Current user:" +user_id)
    my_posts = get_user_posts(user_id)
    return_list = []
    for result in my_posts:
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
    print(json.dumps(return_list))
    return json.dumps(return_list)


@app.route('/createPost', methods=['POST'])
def make_post_for_user():
    print("Creating a post")
    post_json = request.get_json()
    print(post_json)

    # TODO: Get user name from frontend, and generate postID
    user_id = post_json["UserName"]
    post_id = str(uuid.uuid4())
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
    attractionid = str(uuid.uuid4())
    print("Sending post")
    result = add_post(post_id, upvotes, downvotes, description, user_id)
    print("Created post")
    print("Sending attraction")
    result1 = add_attraction(attractionid, latitude, longitude, name, time, cost, rating, post_id)
    insert_recommend_location(tag_list, (latitude, longitude))
    print("Created attraction")
    return json.dumps(result)


@login_manager.user_loader
def load_user(user_id):
    """
    Method to load user given user_id
    :param user_id: User ID
    :return: User object
    """
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        cur.execute(
            "SELECT userId FROM User WHERE u.UserID = ?", (user_id,))
        user = cur.fetchall()
        connection.close()
        if user is None:
            return None
        return User(user_id)
    except sqlite3.Error as err:
        print("Error:" + err.args[0])


@app.route('/deletePost', methods=['POST'])
def delete_post_by_id():
    delete_json = request.get_json()
    print(delete_json)
    post_id = delete_json["PostID"]
    print(post_id)
    result = remove_post(post_id)
    return json.dumps(result)


@app.route('/editPost', methods=['POST'])
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
    return json.dumps("Success")


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
    app.run(host = '0.0.0.0')
    # app.run(debug=True)