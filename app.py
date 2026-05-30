from flask import Flask,request,jsonify,make_response,redirect,url_for
from datetime import date, datetime
import mysql.connector
from flask_cors import CORS
from werkzeug.security import generate_password_hash,check_password_hash
import jwt
import os
from datetime import datetime,timedelta


def get_conn():
    conn = mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "mysql123",
        database = "food"
        )
    return conn

app = Flask(__name__)
CORS(app)

app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY")

@app.route("/signup",methods = "POST")
def signup():
    signup_data = request.get_json()

    if not signup_data:
        return jsonify({"error":"bad request"}),400
    

    if "email" not in signup_data or "password" not in signup_data:
        return jsonify({"error":"bad request"}),400
    
    email = signup_data.get('email')
    password = signup_data.get('password')

    hash_password = generate_password_hash(password)

  
    if email.endswith("@gmail.com") == False:
        return jsonify({"error":"Invalid email"}),400
    
    connection = get_conn()
    c = connection.cursor()

    c.execute("SELECT email FROM customers WHERE email = %s",(email))
    result = c.fetchone()

    if result:
        return jsonify({"error":"Account already exists with this email"}),409
    
    if  not result:
        c.execute("INSERT INTO customers(email,password) VALUES(%s,%s)",(email,hash_password))

    connection.commit()
    connection.close()

    jwt_token = jwt.encode({
            'email':email,
            'exp': datetime.utcnow() + timedelta(hours=1)
            }, app.config['SECRET_KEY'], algorithm='HS256')
    
    response = make_response(
        redirect(url_for('foods'))
        )
                
    response.set_cookie(
        'token',
        jwt_token,
        httponly=True,
        secure=True,
        samesite='Lax'
        )

    return response

def validate_active_token(email,token):
    jwt_token =  token
    email_id = email

    if not  email_id or not jwt_token:
        return "Token,email is required"
     
    jwt_token_data = jwt.decode({
        "token":jwt_token,
        "exp": datetime.utcnow() + timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
        )
    
    if "email" not in jwt_token_data:
        return "Invalid token"
    
    token_email = jwt_token_data.get('email')

    if email_id.lower() == token_email.lower():
        return "User already authenticated"
    
    else:
        return "User not authenticated yet."

    

@app.route("/signin", methods=["POST"])
def signin():

    token = request.cookies.get('token')
    signin_data = request.get_json()

    if not signin_data:
        return jsonify({"error": "Bad request"}), 400

    email = signin_data.get("email")
    password = signin_data.get("password")

    if not email or not password:
        return jsonify({"error": "Email and password required"}), 400

    connection = get_conn()
    c = connection.cursor()

    c.execute(
        "SELECT password FROM customers WHERE email = %s",
        (email,)
    )

    result = c.fetchone()

    if not result:
        connection.close()
        return jsonify({"error": "Invalid email or password"}), 401
    
    if token:
        validate_active_token(email,token)

    stored_password = result[0]

    if not check_password_hash(stored_password, password):
        connection.close()
        return jsonify({"error": "Invalid email or password"}), 401

    jwt_token = jwt.encode(
        {
            "email": email,
            "exp": datetime.utcnow() + timedelta(hours=1)
        },
        app.config['SECRET_KEY'],
        algorithm='HS256'
    )

    response = make_response(
        redirect(url_for('foods'))
    )

    response.set_cookie(
        "token",
        jwt_token,
        httponly=True,
        secure=True,
        samesite="Lax"
    )

    connection.close()

    return response




    
@app.route("/foods")
def foods():
    json_data = []
  
    connection = get_conn()
    c = connection.cursor()

    c.execute("SELECT * FROM foods")
    foods = c.fetchall()

    print(foods)
    
    if foods:
        for food in foods:
        
            json_dict = {"food_id":food[0],"food_name":food[1],"description":food[2],
                         "food_type":food[3],"food_price":food[4]}
            json_data.append(json_dict)
           
        connection.close()

        return jsonify(json_data),200
    else:
        return jsonify({"error":"no food made yet."}),200
    


@app.route("/order",methods = ["POST"])
def order():

    
    data = request.get_json()
    mandatory_fields = ["item_id","cust_id","location","quantity"]

    for key in mandatory_fields:
        if key not in data:
            return jsonify({"error":"bad request"}),400
    
    for key in mandatory_fields:
        if data.get(key)  ==  "" or  data.get(key) == 0:
            return jsonify({"error":"Bad request"}),400
        

    item_id = data.get('item_id')
    cust_id = data.get('cust_id')
    location = data.get('location')
    quantity = data.get('quantity')


    # Get current date and time
    current_time = datetime.now()
    print(current_time)


    connection  = get_conn()
    c = connection.cursor()



    c.execute("SELECT food_id FROM foods WHERE food_id = %s",(item_id,))
    result1 = c.fetchone()
    c.execute("SELECT cust_id FROM customers WHERE cust_id = %s",(cust_id,))
    result2 = c.fetchone()

    if result1 and result2:
        c.execute('''INSERT INTO orders(item_id,quantity,ordered_by,ordered_at,location) VALUES(%s,%s,%s,%s,%s)''',
                  (item_id,quantity,cust_id,current_time,location))
        
        connection.commit()
        
        return jsonify({"success":"order succesfully placed"}),200
    
    else:
        return jsonify({"error":"Bad request"}),400
    



if __name__  == "__main__":
    app.run(debug = True)


 