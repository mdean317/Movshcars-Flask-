from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination
from flask_cors import CORS
from app.models.category import Category
from app.models.movie import Movie
from app.models.user import User

userNominations = Blueprint('userNominations', __name__, url_prefix='/usernoms')
CORS(userNominations)

@userNominations.route('/add', methods=['POST'])
def addUserNomination():
    
    print("in add")
    try:

        data = request.get_json()
        user = User.query.filter_by(username=data['username']).first()

        newUserNomination = UserNomination(user_id=user.user_id, nomination_id=data['nomination_id'], didWin=data['didWin'])
        print(newUserNomination)
        db.session.add(newUserNomination)
        db.session.commit()
        return jsonify({"message": "Movie added successfully"}), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500

@userNominations.route('/')
def getUserNomsByYearAndCategory():

    year_arg= request.args.get('year', type=int)
    category_id_arg = request.args.get('category', type=int)
    username = request.args.get('username', type=str)

    user = User.query.filter_by(username=username).first()
    userNoms = (db.session.query(Nomination)
                .join(UserNomination, UserNomination.nomination_id == Nomination.nomination_id)
                .filter(UserNomination.user_id==user.user_id, Nomination.category_id == category_id_arg, Nomination.year == year_arg)
                .add_columns(UserNomination.didWin, UserNomination.user_id)
                .all()
                )
    
    result = []
    for nom, didWin, user_id in userNoms:
        
        movieObj = db.session.query(Movie).filter_by(imdb_id=nom.movie_id).first()
       
        categoryObj = db.session.query(Category).filter_by(category_id=nom.category_id).first()
      
        result.append({
            'nomination_id': nom.nomination_id,
            'year': nom.year,
            'category': categoryObj.to_dict(),
            'movie': movieObj.to_dict(),
            'nominee': nom.nominee,
            'user_id': user_id,
            'didWin': didWin
        })

    return jsonify(result)
 
@userNominations.route('/delete/<userid>/<nominationid>', methods=['DELETE'])
def deleteUserNomination(userid, nominationid):
    try:

        nomToDelete = UserNomination.query.filter_by(user_id=userid, nomination_id=nominationid).first()
        
        if nomToDelete:
            db.session.delete(nomToDelete)
            db.session.commit()
            return jsonify({"message": "Movie deleted successfully"}), 200

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500