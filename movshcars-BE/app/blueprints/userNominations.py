# Import dependecies
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination
from flask_cors import CORS

# Import necessary DB models
from app.models.category import Category
from app.models.movie import Movie
from app.models.user import User

# Initiate bluprint
userNominations = Blueprint('userNominations', __name__, url_prefix='/usernoms')

# Apply CORS to blueprint
CORS(userNominations)

# Logic for add user nomination to DB route 
@userNominations.route('/add', methods=['POST'])
def addUserNomination():
    
    try:

        # Parse the request data
        data = request.get_json()

        # Get User object from db based the request data
        user = User.query.filter_by(username=data['username']).first()

        # Create corrolating UserNom Dict from db
        newUserNomination = UserNomination(user_id=user.user_id, nomination_id=data['nomination_id'], didWin=data['didWin'])

        # Add UserNom to db
        db.session.add(newUserNomination)
        db.session.commit()

        # Return successful message
        return jsonify({"message": "Movie added successfully"}), 201

    # Catch exception
    except Exception as error:
        
        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500

# Probably most common function to use - getting user nominations by year and category. 
@userNominations.route('/')
def getUserNomsByYearAndCategory():

    try:
        # Get variables from request
        year_arg= request.args.get('year', type=int)
        category_id_arg = request.args.get('category', type=int)
        username = request.args.get('username', type=str)

        # Get user from db
        user = User.query.filter_by(username=username).first()

        # Get all user nominations which meet the criteria from the db, based on request variables
        userNoms = (db.session.query(Nomination)
                    .join(UserNomination, UserNomination.nomination_id == Nomination.nomination_id)
                    .filter(UserNomination.user_id==user.user_id, Nomination.category_id == category_id_arg, Nomination.year == year_arg)
                    .add_columns(UserNomination.didWin, UserNomination.user_id)
                    .all()
                    )
        
        # Initiate return array
        result = []

        # Loop to add each user nomination and all it's info to return array
        for nom, didWin, user_id in userNoms:
            
            # For each nom, get their corrosponding movie and category db data
            movieObj = db.session.query(Movie).filter_by(imdb_id=nom.movie_id).first()
            categoryObj = db.session.query(Category).filter_by(category_id=nom.category_id).first()

            # Add user nomination to return array
            result.append({
                'nomination_id': nom.nomination_id,
                'year': nom.year,
                'category': categoryObj.to_dict(),
                'movie': movieObj.to_dict(),
                'nominee': nom.nominee,
                'user_id': user_id,
                'didWin': didWin
            })

        # Return array with query results
        return jsonify(result)

    # Catch exception
    except Exception as error:

        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500
    
# Delete user nom logic
@userNominations.route('/delete/<userid>/<nominationid>', methods=['DELETE'])
def deleteUserNomination(userid, nominationid):
    try:

        # Delete user nom based on the dynamic paramters in route 
        nomToDelete = UserNomination.query.filter_by(user_id=userid, nomination_id=nominationid).first()
        
         # If not found, Return not found message
        if not nomToDelete:
            return jsonify({"error": "Nomination not found"}), 404
        
        # If found, delete and return success message
        db.session.delete(nomToDelete)
        db.session.commit()
        return jsonify({"message": "Movie deleted successfully"}), 200
    
    # Catch exception
    except Exception as error:

        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500