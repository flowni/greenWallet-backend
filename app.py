from flask import Flask, jsonify, render_template, request
from flaskext.mysql import MySQL
import os
import json
import queries
from decimal import Decimal
import datetime
import utils



class DataEncoder(json.JSONEncoder):
  def default(self, obj):
    if isinstance(obj, Decimal):
      return str(round(obj,4))
    elif isinstance(obj, datetime.datetime):
      return str(obj)
    return json.JSONEncoder.default(self, obj)


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

@app.route("/purchase/", methods=['POST'])
def checkout_purchase_from_store():
    content = request.json

    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(queries.search_user_with_barcode.format(content["membership_no"]))
    user = cursor.fetchone()
    if user is None:
        response = app.response_class(response=jsonify({"error":"Customer not found"}),
                                status=403,
                                mimetype='application/json')

    uid = user[0]
    print(f"user:{uid}")
    ucoins_lifetime = user[1]
    ubalance = user[2]
    #recording the transaction details in purchases
    cursor.execute(queries.insert_purchases_query.format(uid,content['purchase_time'],
    content['partner_id']))
    purchase_id = cursor.lastrowid                        
    
    print(f"purchase_id:{purchase_id}")
    # calculating total amounts, coins earned and updating purchase_product_mapping
    # total_amount = 0
    total_coins = 0
    for product in content["products"]:
        barcode = product["barcode"]
        cursor.execute(queries.search_product_with_barcode.format(barcode))
        p = cursor.fetchone()
        if p is None:
            print(f"Barcode {barcode} doesn't exist in database, skipping product")
            continue
        p_id = p[0]
        product_score = utils.calculate_green_score(barcode)
        coins_earned = round(product['amount']*product_score)
        total_coins += coins_earned
        # total_amount += product['amount']
        cursor.execute(queries.insert_purchase_product_query.format(purchase_id,
                            p_id,
                            product['product_qty'],
                            product['amount'],
                            coins_earned))

    #update user coinss
    ubalance = ubalance + total_coins
    ucoins_lifetime += total_coins

    cursor.execute(queries.update_user_coins.format(ucoins_lifetime, ubalance, uid))


    return jsonify({"status":"received"})

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
    data = [{"purchase_id":x[0],
             "product_time":x[1],
             "partner_id": x[2],
             "partner_name":x[3],
             "total_amount":x[4],
             "total_coins":x[5],
             "partner_icon_url":x[6]} for x in data]
    return app.response_class(response=json.dumps(data, cls=DataEncoder),
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
             "coins_earned":x[4],
             "image_url": x[5]} for x in data]
    result['products'] = data

    response = app.response_class(response=json.dumps(result, cls=DataEncoder),
                                status=200,
                                mimetype='application/json')
    return response

@app.route("/product_info/<product_id>")
def get_product_info(product_id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute(queries.product_info_query.format(product_id))
    data = cursor.fetchone()
    data = {k:v for (k,v) in zip(utils.products_columns, data)}
    data['green_score']= utils.calculate_green_score(data["barcode"])

    response = app.response_class(response=json.dumps(data, cls=DataEncoder),
                                status=200,
                                mimetype='application/json')
    return response