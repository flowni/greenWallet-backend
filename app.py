from flask import Flask
from flaskext.mysql import MySQL
import os
from dotenv import load_dotenv
import json

app = Flask(__name__)
mysql = MySQL()
app.config['MYSQL_DATABASE_USER'] = os.getenv('MYSQL_DATABASE_USER')
app.config['MYSQL_DATABASE_PASSWORD'] = os.getenv('MYSQL_DATABASE_PASSWORD')
app.config['MYSQL_DATABASE_DB'] = os.getenv('MYSQL_DATABASE_DB')
app.config['MYSQL_DATABASE_HOST'] = os.getenv('MYSQL_DATABASE_HOST')
mysql.init_app(app)

@app.route("/")
def hello():
    print("Handling request to home page.2")
    return "Hello, Azure!"

@app.route("/purchase")
def checkout_purchase_from_store():
    # receive a json, barcodes and quantities, user_id
    # update tables
    return

@app.route("/purchases/:user_id")
def get_purchases_of_user(user_id):
    # return all purchases of a user
    return

@app.route("/users")
def get_users():
    print("read: " + os.getenv('MYSQL_DATABASE_PASSWORD'))
    # return all users
    conn = mysql.connect()
    cursor = conn.cursor()

    cursor.execute("select * from users")
    data = cursor.fetchall()
    print(data)
    # data = {'name': 'nabin khadka'}
    response = app.response_class(response=json.dumps(data),
                                status=200,
                                mimetype='application/json')

    return response

