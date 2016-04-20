# from flask import Flask, request
# from flask.ext.mysql import MySQL
# mysql = MYSQL()
# app.config['MYSQL_DATABASE_USER'] = 'root'
# app.config['MYSQL_DATABASE_PASSWORD'] = ''
# app.config['MYSQL_DATABASE_DB'] = 'touristy_database'
# app.config['MYSQL_DATABASE_HOST'] = 'localhost'
# mysql.init_app(app)
import os
import sqlite3
from User import *
from geopy.distance import vincenty

from app import login_manager

file_name = os.path.join(os.path.dirname(__file__), 'touristy_database2.db')


def add_attraction(attractionid, latitude, longitude, name, time, cost, rating, postID):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        print("Connected to database")
        cur.execute(
            "INSERT INTO Attractions (AttractionID, Latitude, Longitude, Name, time, cost, rating, postID) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (attractionid, latitude, longitude, name, time, cost, rating, postID))
        print('Adding attraction executed')
        connection.close()
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    print('hey')


def edit_attraction(json_object, aid):
    try:
        print("Editing attraction")
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        if json_object.get("Longitude"):
            l = json_object.get("Longitude")
            cur.execute("UPDATE Attractions SET Longitude=? WHERE postID=?", (l, aid))

        if json_object.get("Latitude"):
            l = json_object.get("Latitude")
            cur.execute("UPDATE Attractions SET Latitude=? WHERE postID=?", (l, aid))

        if json_object.get("Name"):
            l = json_object.get("Name")
            cur.execute("UPDATE Attractions SET Name=? WHERE postID=?", (l, aid))

        if json_object.get("AttractionID"):
            l = json_object.get("AttractionID")
            cur.execute("UPDATE Attractions SET AttractionID=? WHERE postID=?", (l, aid))

        if json_object.get("time"):
            l = json_object.get("time")
            cur.execute("UPDATE Attractions SET time=? WHERE postID=?", (l, aid))

        if json_object.get("cost"):
            l = json_object.get("cost")
            cur.execute("UPDATE Attractions SET cost=? WHERE postID=?", (l, aid))

        if json_object.get("PostID"):
            l = json_object.get("PostID")
            cur.execute("UPDATE Attractions SET postID=? WHERE postID=?", (l, aid))

        if json_object.get("rating"):
            l = json_object.get("rating")
            cur.execute("UPDATE Attractions SET rating=? WHERE postID=?", (l, aid))

        print('hey')
        connection.close()
    except sqlite3.Error as err:
        print("Error:" + err.args[0])


def remove_attraction(aid):
    connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
    cur = connection.cursor()

    cur.execute("DELETE FROM Attractions WHERE postID=?", aid)

    print('hey')
    connection.close()


def add_post(postID, upvotes, downvotes, description, userid):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        print(type(postID))
        print(type(upvotes))
        print(type(downvotes))
        print(type(description))
        print(type(userid))
        print("Connected to database")
        cur.execute("INSERT INTO Posts (postID, Upvotes, Downvotes, Description, UserID) VALUES (?, ?, ?, ?, ?)",
                    (postID, upvotes, downvotes, description, userid))
        print('Adding post executed')
        connection.close()
    except sqlite3.Error as err:
        print("Error:" + err.args[0])


def edit_post(json_object, pid):
    try:
        print(json_object)
        print("Trying to edit")
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        if json_object.get("PostID"):
            print("Getting postid")
            l = json_object.get("PostID")
            print("postID:" + str(l))
            cur.execute("UPDATE Posts SET postID=? WHERE postID=?", (l, pid))

        if json_object.get("Upvotes"):
            l = json_object.get("Upvotes")
            cur.execute("UPDATE Posts SET Upvotes=? WHERE postID=?", (l, pid))

        if json_object.get("Downvotes"):
            l = json_object.get("Downvotes")
            cur.execute("UPDATE Posts SET Downvotes=? WHERE postID=?", (l, pid))

        if json_object.get("Description"):
            l = json_object.get("Description")
            cur.execute("UPDATE Posts SET Description=? WHERE postID=?", (l, pid))

        if json_object.get("UserID"):
            l = json_object.get("UserID")
            cur.execute("UPDATE Posts SET userID=? WHERE postID=?", (l, pid))
        connection.close()
    except sqlite3.Error as err:
        print("Error:" + err.args[0])


def remove_post(pid):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        cur.execute("DELETE FROM Attractions WHERE postID=?", (pid,))
        cur.execute("DELETE FROM Posts WHERE postID=?", (pid,))
        connection.close()
        return ["OK", "Success"]
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
        return ["Error", err.args[0]]


def get_user_posts(user_id):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.Time, a.Cost, a.Rating, p.postID FROM User u INNER JOIN Posts p ON u.userID = p.userID INNER JOIN Attractions a ON p.postID = a.postID WHERE u.userID = ?",
            (user_id,))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def add_user(userid, name, email, phone_no, password, no_of_posts):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        print('Inserting!')
        cur.execute("INSERT INTO User (userID, Name, Email, phonenum, Password, numposts) VALUES (?, ?, ?, ?, ?, ?)",
                    (userid, name, email, phone_no, password, no_of_posts))
        print('Inserted!')
        connection.close()
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
        return ["Error", err.args[0]]
    return ["OK", "Successful", userid]


def remove_user(uid):
    connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
    cur = connection.cursor()
    cur.execute("DELETE FROM User WHERE userID=?", uid)
    print('hey')
    connection.close()


def login_user_database(user_id, password_user):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        cur.execute(
            "SELECT Password FROM User WHERE userID=?",
            (user_id,))
        print("Query executed!")
        password_database = cur.fetchone()[0]
        print('Database password:' + password_database)
        if password_database is None:
            result = ["Error", "User not found!"]
        else:
            is_valid_password = User.validate_login(password_database, password_user)
            if is_valid_password:
                result = ["OK", "Success", user_id]
            else:
                result = ["Error", "Incorrect password"]
        connection.close()

        return result


    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long(latitude, longitude):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        print('Hey')
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID "
            "FROM Posts AS p INNER JOIN Attractions AS a ON p.postID=a.postID WHERE a.Latitude=? AND a.Longitude=?",
            (latitude, longitude))
        print('Hey')
        result_list = cur.fetchall()
        print(result_list)
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_rating(latitude, longitude, rating):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.rating>=? ORDER BY a.rating DESC",
            (latitude, longitude, rating))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_cost(latitude, longitude, cost):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.cost<=?  ORDER BY a.cost ASC",
            (latitude, longitude, cost))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_cost_rating(latitude, longitude, cost, rating):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.cost<=? AND a.rating>=? ORDER BY a.rating DESC",
            (latitude, longitude, cost, rating))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_time(latitude, longitude, time):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.time<=? ORDER BY a.time ASC",
            (latitude, longitude, time))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_time_rating(latitude, longitude, time, rating):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.time<=? AND a.rating>=?  ORDER BY a.rating DESC",
            (latitude, longitude, time, rating))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_time_cost(latitude, longitude, time, cost):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.time<=? AND a.cost<=?  ORDER BY a.cost ASC",
            (latitude, longitude, time, cost))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def select_lat_long_time_cost_rating(latitude, longitude, time, cost, rating):
    try:
        connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
        cur = connection.cursor()
        # cur.execute("SELECT * FROM Attractions WHERE Latitude=? AND Longitude=?", (latitude, longitude))
        cur.execute(
            "SELECT p.Upvotes, p.Downvotes, p.Description, p.userID, a.Name, a.time, a.cost, a.rating, p.postID FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE a.Latitude=? AND a.longitude=? AND a.time<=? AND a.cost<=? AND a.rating>= ? ORDER BY a.rating DESC",
            (latitude, longitude, time, cost, rating))
        result_list = cur.fetchall()
        connection.close()
        return result_list
    except sqlite3.Error as err:
        print("Error:" + err.args[0])
    return []


def heatmap(latitude, longitude):
    connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
    cur = connection.cursor()
    cur.execute("SELECT * FROM Attractions")
    rows = cur.fetchall()
    point_location = (latitude, longitude)
    min_dist1 = 10000000
    min_dist2 = 1000000000
    min_dist3 = 10000000000
    min_dist4 = 1000000000000

    min_row1 = None
    min_row2 = None
    min_row3 = None
    min_row4 = None

    for row in rows:
        dest_location = (row[1], row[2])
        dist = float(vincenty(point_location, dest_location).miles)
        # print(str(dist) + " " + str(row[0]))

        if min_dist1 > dist:
            min_dist4 = min_dist3
            min_row4 = min_row3
            min_dist3 = min_dist2
            min_row3 = min_row2
            min_dist2 = min_dist1
            min_row2 = min_row1
            min_dist1 = dist
            min_row1 = row

        if min_dist2 > dist and dist != min_dist1:
            min_dist4 = min_dist3
            min_row4 = min_row3
            min_dist3 = min_dist2
            min_row3 = min_row2
            min_dist2 = dist
            min_row2 = row

        if min_dist3 > dist and dist != min_dist1 and dist != min_dist2:
            min_dist4 = min_dist3
            min_row4 = min_row3
            min_dist3 = dist
            min_row3 = row

        if min_dist4 > dist and dist != min_dist1 and dist != min_dist2 and dist != min_dist3:
            min_dist4 = dist
            min_row4 = row

    # print("\n" + str(min_row3[1]))

    lat1 = min_row1[1]
    long1 = min_row1[2]
    cur.execute(
        "SELECT * FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE Latitude='{}' AND Longitude='{}'".format(
            lat1, long1))
    rows1 = cur.fetchall()
    len1 = len(rows1)

    lat2 = min_row2[1]
    long2 = min_row2[2]
    cur.execute(
        "SELECT * FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE Latitude='{}' AND Longitude='{}'".format(
            lat2, long2))
    rows2 = cur.fetchall()
    len2 = len(rows2)

    lat3 = min_row3[1]
    long3 = min_row3[2]
    cur.execute(
        "SELECT * FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE Latitude='{}' AND Longitude='{}'".format(
            lat3, long3))
    rows3 = cur.fetchall()
    len3 = len(rows3)

    lat4 = min_row4[1]
    long4 = min_row4[2]
    cur.execute(
        "SELECT * FROM Posts p INNER JOIN Attractions a ON p.postID=a.postID WHERE Latitude='{}' AND Longitude='{}'".format(
            lat4, long4))
    rows4 = cur.fetchall()
    len4 = len(rows4)

    # print(len4)

    data = [(lat1, long1, len1), (lat2, long2, len2), (lat3, long3, len3), (lat4, long4, len4)]
    # for tuple in data:
    # print(tuple)
    return data


def check_all_tags(latitude, longitude, tags_arr):
    connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
    cur = connection.cursor()

    cur.execute("PRAGMA table_info(Tags)")

    arr = cur.fetchall()
    list = [i[1] for i in arr]

    cur.execute("SELECT * From Tags WHERE Latitude = '{}' AND Longitude = '{}'".format(latitude, longitude))
    latlongarr = cur.fetchall()

    if (len(latlongarr) == 0):
        cur.execute("INSERT INTO Tags (Latitude, Longitude) VALUES ('{}', '{}')".format(latitude, longitude))

    for tag in tags_arr:
        if tag not in list:
            cur.execute("ALTER TABLE Tags ADD COLUMN '{}' INTEGER DEFAULT(0)".format(tag))
            cur.execute(
                "UPDATE Tags SET '{}' = 1 WHERE Latitude = '{}' AND Longitude = '{}'".format(tag, latitude, longitude))
            list.append(tag)
        if tag in list:
            cur.execute(
                "UPDATE Tags SET '{}' = 1 WHERE Latitude = '{}' AND Longitude = '{}'".format(tag, latitude, longitude))


def get_tag_columns():
    connection = sqlite3.connect(file_name, isolation_level=None, timeout=11)
    cur = connection.cursor()

    cur.execute("SELECT * FROM Tags")
    arr = cur.fetchall()

    latlong = []
    others = []

    for entry in arr:
        tuple1 = (str(entry[0]), str(entry[1]))
        latlong.append(tuple1)

        tuple2 = entry[2:]
        others.append(tuple2)

    return [latlong, others]


if __name__ == '__main__':
    print(select_lat_long(48.8582, 2.2945))
