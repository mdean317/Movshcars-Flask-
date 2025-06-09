# Import dependecies 
from flask import Blueprint, request, jsonify, Response
from flask_cors import CORS
from flask_login import login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

# Import DB 
from app.extensions import db

# Import User DB model/schema
from app.models.user import User

# Initiate bluprint
auth = Blueprint('auth', __name__, url_prefix='/auth')

# Apply CORS to blueprint
CORS(auth)

# Logic for login route
@auth.route('/login', methods=['POST'])
def login():
    try:
        # parse the request data
        data = request.get_json()

        # get the needed variables from the request
        email = data['email']
        password = data['password']
        remember = data['remember']

        # check if user exists in db by email
        user = User.query.filter_by(email=email).first()

        # if user doesn't exist, alert user
        if not user:
            return jsonify({"error": 'User does not exist, please create an account'}), 401
        
        # if user exists, take the user-supplied password, hash it, and compare it to the hashed password in the db
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Incorrect password"}), 401

        # if user exists and password is correct, log user in
        login_user(user, remember=remember)

        # return user dict
        return jsonify(user.to_dict())
    
    # catch exceptions
    except Exception as error:
        print(error)
        return jsonify({'error': str(error)}), 500

# Logic for sign up route
@auth.route('/signup', methods=['POST'])
def signup_post():
    try:
        # parse the request data
        data = request.get_json()

        # get the needed variables from the data
        email = data['email']
        username = data['username']
        password = data['password']

        # check if a user exists with submitted email
        emailCheck = User.query.filter_by(email=email).first() 
        
        # if email is found, alert user
        if emailCheck: 
            return jsonify({"error": 'an account already exists with this email'}), 401
        
        # check if a user exists with submitted username
        usernameCheck = User.query.filter_by(username=username).first()

        # if username is found, alert user
        if usernameCheck: # if a user is found, we want to redirect back to signup page so user can try again
            return jsonify({"error": 'an account already exists with this username'}), 401

        # if these checks have passed, create a new user with a hashed password. 
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        # return success response 
        return Response(status=200)
    
    # catch exceptions
    except Exception as error:
        print(error)
        return jsonify({'error': str(error)}), 500

# Logic for log out route
@auth.route('/logout')
def logout():
    try:
        # use package function to log out
        logout_user()

        # return success indication
        return Response(status=200)

    # catch exceptions
    except Exception as error:
        print(error)
        return jsonify({'error': str(error)}), 500

# ping check route
@auth.route("/ping")
def ping():
    return "pong", 200
