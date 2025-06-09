# Import dependencies 
import os
from flask import Flask
from flask_cors import CORS
from app.extensions import db
from app.blueprints import blueprints 
from app.init_db_data import init_db_data
from flask_login import LoginManager
from app.models.user import User
from dotenv import load_dotenv

# Set absolute path to the folder holding this file. 
basedir = os.path.abspath(os.path.dirname(__file__))

# Creates a Flask application instance as 'main'
app = Flask(__name__)

# Sets the database URI, and the path to the DB file.
app.config['SQLALCHEMY_DATABASE_URI'] =\
           'sqlite:///' + os.path.join(basedir, 'movshcars.db')

# Disables tracks object changes 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initializes the SQLAlchemy extension
db.init_app(app)

# Applies CORS to request methods and any origin.
CORS(app, resources={r"/*": {"origins": "*"}}, allow_headers="*", methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"])

# Loads environment variables
load_dotenv()

# Sets secret key from loaded environment variables
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')

# Check that the secret key was successfully loaded
if not app.secret_key:
    
    # Raise error if it wasn't
    raise ValueError("No FLASK_SECRET_KEY set! Please set the environment variable.")

# Load all blueprints into app instances
for bp in blueprints:
    app.register_blueprint(bp)

# Create an instance of flasks login manager
login_manager = LoginManager()

# Defines the route users will be sent to if they try to access a restricted page
login_manager.login_view = 'auth.login'

# Connect login manager with app instance 
login_manager.init_app(app)

# Define how the login manager will retrieve users. 
@login_manager.user_loader

# Get the user id pf the user trying to log in, and return the user dict assoicated with it.
def load_user(user_id):
        return User.query.get(int(user_id))

# Run the db commands in the context of the instnatiated app 
with app.app_context():
        
        # Log the tables defined in your models.
        print("Tables detected:", db.metadata.tables.keys())

        # Log the path where the db file is created
        print("DB will be created at:", os.path.abspath("movshcars.db"))

        # Create db tables if they don't already exist
        db.create_all() 

        # Initiate the db data
        init_db_data()   

# Run the app
if __name__ == '__main__':
        app.run(host='0.0.0.0', port=4000, debug=True)