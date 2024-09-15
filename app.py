from flask import Flask, request, jsonify
from flask_bcrypt import Bcrypt
from flask_mysqldb import MySQL
import re
from flask_cors import CORS 

app = Flask(__name__)
import json

CORS(app)

# Configuration for MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Add your MySQL password
app.config['MYSQL_DB'] = 'encrypted'

# Initialize MySQL and Bcrypt for password hashing
mysql = MySQL(app)
bcrypt = Bcrypt(app)

# Function to create users table
def create_users_table():
    with app.app_context():
        conn = mysql.connection
        cursor = conn.cursor()
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INT AUTO_INCREMENT PRIMARY KEY,
            fullname VARCHAR(150) NOT NULL,
            username VARCHAR(80) UNIQUE NOT NULL,
            phone_number VARCHAR(10) UNIQUE NOT NULL,
            address VARCHAR(200) NOT NULL,
            email VARCHAR(120) UNIQUE NOT NULL,
            password VARCHAR(200) NOT NULL
        )
        """)
        conn.commit()
        cursor.close()

create_users_table()

# Validation for phone number (must be 10 digits) and email (@gmail.com)
def validate_phone_number(phone_number):
    return len(phone_number) == 10 and phone_number.isdigit()

def validate_email(email):
    return email.endswith('@gmail.com')

# POST: Add a new user
@app.route('/user', methods=['POST'])
def add_user():
    data = request.get_json()
    
    print(data, "to convert")
    
    # data = json.loads(dataString)
    
    print("Hit " ,data)
    
    fullname = data.get('fullname')
    username = data.get('username')
    phone_number = data.get('phone_number')
    address = data.get('address')
    email = data.get('email')
    password = data.get('password')

    # Validate phone number and email
    if not validate_phone_number(phone_number):
        return jsonify({"error": "Phone number must be 10 digits"}), 400
    if not validate_email(email):
        return jsonify({"error": "Email must end with @gmail.com"}), 400

    # Encrypt the password
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

    # Insert the new user into the database
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        cursor.execute("""
        INSERT INTO users (fullname, username, phone_number, address, email, password)
        VALUES (%s, %s, %s, %s, %s, %s)
        """, (fullname, username, phone_number, address, email, hashed_password))
        conn.commit()
        return jsonify({"success": True, "message": f"User {fullname} added successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Username, email, or phone number already exists"}), 400
    finally:
        cursor.close()

# Login
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    
    password = data.password
    
    print("Login Data " , data)
    
    hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
    username = data.username
    
    conn = mysql.connection
    cursor = conn.cursor()
    try:
        user = cursor.execute("""
        SELECT FROM users WHERE username=%s AND password=%s
        """, (username, hashed_password))
        print("user ", user)
        conn.commit()
        return jsonify({"success": True, "message": "Logged In"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": "Username, email, or phone number already exists"}), 400
    finally:
        cursor.close()
    

# GET: Retrieve all users
@app.route('/users', methods=['GET'])
def get_users():
    conn = mysql.connection
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT fullname, username, phone_number, address, email FROM users")
    users = cursor.fetchall()
    cursor.close()

    return jsonify(users)

# GET: Retrieve a specific user by username
@app.route('/user/<username>', methods=['GET'])
def get_user(username):
    conn = mysql.connection
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT fullname, username, phone_number, address, email FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    cursor.close()

    if not user:
        return jsonify({"error": "User not found"}), 404

    return jsonify(user)

# Root route for testing
@app.route('/')
def index():
    return "Welcome to the API!"

if __name__ == '__main__':
    app.run(debug=True)
