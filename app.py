from flask import Flask, redirect, url_for, render_template
from flaskext.mysql import MySQL
import os
import json
import queries
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
    conn = mysql.connect()
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


@app.route("/purchases/<user_id>")
def get_purchases_of_user(user_id):
    # return all purchases of a user
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(queries.all_purchases_query.format(user_id))
    data = cursor.fetchall()
    return app.response_class(response=json.dumps(data),
    status=200,
    mimetype='application/json')

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


@app.route("/purchase_details/<purchase_id>")
def get_purchase_details(purchase_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(queries.purchase_details_query_1.format(purchase_id))
    data = cursor.fetchone()
    result = {
        "purchase_time":str(data[0]),
        "partner_id":data[1],
        "partner_name":data[2],
        "total_amount":data[3],
        "total_coins_earned":data[4] 
    }
    cursor.execute(queries.purchase_details_query_2.format(purchase_id))
    data = cursor.fetchall()
    data = [{"product_id":x[0],
             "product_name":x[1],
             "quantity": x[2],
             "total_amount":x[3],
             "coins_earned":x[4]} for x in data]
    result['products'] = data

    response = app.response_class(response=json.dumps(result),
                                status=200,
                                mimetype='application/json')
    return response