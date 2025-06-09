# Import dependecies 
from flask import Blueprint, jsonify
from app.extensions import db
from flask_cors import CORS
from app.models.category import Category

# Initiate bluprint
categories = Blueprint('categories', __name__, url_prefix='/categories')

# Apply CORS to blueprint
CORS(categories)

# Logic for index route - getting all categories 
@categories.route('/index')
def getAllCategories():

    # Get all cats in db
    allCategories = (db.session.query(Category).all())

    # Initiate return array
    result = []

    # Append each category dictionary into return array
    for cat in allCategories:
        result.append(cat.to_dict())

    # Return arrays
    return jsonify(result)
 