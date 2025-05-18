from flask import Blueprint, jsonify
from app.extensions import db
from flask_cors import CORS
from app.models.category import Category

categories = Blueprint('categories', __name__, url_prefix='/categories')
CORS(categories)

@categories.route('/index')
def getAllCategories():
    allCategories = (db.session.query(Category).all())
    result = []
    for cat in allCategories:
        result.append(cat.to_dict())

    return jsonify(result)
 