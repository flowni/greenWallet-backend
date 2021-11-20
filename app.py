from flask import Flask, redirect, url_for, render_template
from flaskext.mysql import MySQL
import os
import json

# from dotenv import load_dotenv

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql.init_app(app)


@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/purchase")
def checkout_purchase_from_store():
    # receive a json, barcodes and quantities, user_id
    # update tables
    return

@app.route("/user/<user_id>")
def get_user_details(user_id):
    cursor = conn.cursor()
    cursor.execute("select * from users where id = {}".format(user_id))
    data = cursor.fetchone()
    json_dict = {
        "id": data[0],
        "name": data[1],
        "email": data[2],
        "barcode": data[3],
        "total_coins_earned": data[4],
        "balance": data[5]
    }
    print(json_dict)

    response = app.response_class(response=json.dumps(json_dict),
                                status=200,
                                mimetype='application/json')
    return response


@app.route("/purchases/:user_id")
def get_purchases_of_user(user_id):
    # return all purchases of a user
    return

@app.route("/users")
def get_users():
    conn = mysql.connect()
    # return all users
    cursor = conn.cursor()
    cursor.execute("select * from users")
    data = cursor.fetchall()
    print(data)
    response = app.response_class(response=json.dumps(data),
                                status=200,
                                mimetype='application/json')

    return response

