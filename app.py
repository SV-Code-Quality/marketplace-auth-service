from flask import Flask, request, jsonify
from flask_cors import CORS
import psycopg2
import os

# MAINTAINABILITY ISSUE: Unused import
import json 
import datetime

app = Flask(__name__)
CORS(app)

# SECURITY ISSUE: Hardcoded secret (SonarQube should detect this)
SECRET_KEY = "super-secret-key-12345"

def get_db_connection():
    # RELIABILITY ISSUE: No proper error handling if DB is down
    conn = psycopg2.connect(
        host="localhost",
        database="marketplace",
        user="marketplace",
        password="marketplace"
    )
    return conn

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # SECURITY ISSUE: SQL Injection vulnerability (using string formatting instead of parameterized queries)
    # This is easy to spot and fix.
    try:
        query = f"INSERT INTO users (username, email, password) VALUES ('{username}', '{email}', '{password}')"
        cur.execute(query)
        conn.commit()
        return jsonify({"message": "User registered successfully"}), 201
    except Exception as e:
        # RELIABILITY ISSUE: Broad exception catch and exposing details (security too)
        return jsonify({"error": str(e)}), 400
    finally:
        cur.close()
        conn.close()

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # SECURITY ISSUE: SQL Injection
    query = f"SELECT * FROM users WHERE username = '{username}' AND password = '{password}'"
    cur.execute(query)
    user = cur.fetchone()
    
    if user:
        # MAINTAINABILITY ISSUE: Returning sensitive data directly
        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user[0],
                "username": user[1],
                "email": user[3]
            }
        }), 200
    else:
        return jsonify({"message": "Invalid credentials"}), 401

if __name__ == '__main__':
    # MAINTAINABILITY ISSUE: Debug mode enabled in production code
    app.run(host='0.0.0.0', port=5001, debug=True)
