from flask import Blueprint, redirect, url_for, request, jsonify, Response
from werkzeug.security import generate_password_hash, check_password_hash
from app.extensions import db
from flask_cors import CORS
from app.models.user import User
from flask_login import login_user, logout_user

auth = Blueprint('auth', __name__, url_prefix='/auth')
CORS(auth)

@auth.route('/login', methods=['POST'])

def login():

    try:
        print('login')
        # login code goes here
        data = request.get_json()
        email = data['email']
        password = data['password']
        remember = True if request.form.get('remember') else False

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"error": 'There is already an account associated with this email'}), 401
        # check if the user actually exists
        # take the user-supplied password, hash it, and compare it to the hashed password in the database
        if not check_password_hash(user.password, password):
            return jsonify({"error": "Invalid login"}), 401

        # if the above check passes, then we know the user has the right credentials
        print("made it here")
        login_user(user, remember=remember)
        print("And... here?")
        return Response(status=200)
    
    except Exception as error:
        print(error)
        return jsonify({'error': str(error)}), 500

@auth.route('/signup', methods=['POST'])
def signup_post():

    try:
      
        # code to validate and add user to database goes here
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
      
        emailCheck = User.query.filter_by(email=email).first() # if this returns a user, then the email already exists in database
        
        if emailCheck: # if a user is found, we want to redirect back to signup page so user can try again
            return jsonify({"error": 'email exists'}), 401
        
        usernameCheck = User.query.filter_by(username=username).first()
        if usernameCheck: # if a user is found, we want to redirect back to signup page so user can try again
            return jsonify({"error": 'username exists'}), 401

        # create a new user with the form data. Hash the password so the plaintext version isn't saved.
        new_user = User(email=email, username=username, password=generate_password_hash(password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(new_user)
        db.session.commit()

        return Response(status=200)
    
    except Exception as error:
        print(error)
        return jsonify({'error': str(error)}), 500


@auth.route('/logout')
def logout():
    try:
        print('logout')
        logout_user()
        return Response(status=200)

    except Exception as error:
        return jsonify({'error': str(error)}), 500

