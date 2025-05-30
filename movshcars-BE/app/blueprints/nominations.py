from flask import Blueprint, request, jsonify
from sqlalchemy import func
from app.extensions import db
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination
from app.models.movie import Movie
from app.models.category import Category
from app.models.user import User
from flask_cors import CORS

nominations = Blueprint('nominations', __name__, url_prefix='/noms')
CORS(nominations)

@nominations.route('/add', methods=['POST'])
def addNomination():
    
    try:
        print('hi')
        data = request.get_json()
        print(data)
        newNomination = Nomination(year=data['year'], category_id=data['category_id'], movie_id=data['movie'], 
                                    nominee=data['nominee'])
        
        print(newNomination)
        db.session.add(newNomination)
        db.session.commit()        

        email = data['email']

        user = User.query.filter_by(email=email).first()
        print(newNomination)

        newUserNomination = UserNomination(user_id=user.user_id, nomination_id=newNomination.nomination_id, didWin=False)

        print(newUserNomination)

        db.session.add(newUserNomination)
        db.session.commit() 

        return jsonify({"message": "Nomination added successfully"}), 201
    
    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500

@nominations.route('/')
def getNomsByYearAndCategory():

    year_arg= request.args.get('year', type=int)
    category_id_arg = request.args.get('category', type=int)

    nomBank = (db.session.query(Nomination)
                .filter(Nomination.category_id == category_id_arg, Nomination.year == year_arg)
                .all()
                )

    result = []

    for nom in nomBank:

        movieObj = db.session.get(Movie, nom.movie_id)
        categoryObj = db.session.get(Category, nom.category_id)
        
        result.append({

            'nomination_id': nom.nomination_id,
            'year': nom.year,
            'category': categoryObj.to_dict(),
            'movie': movieObj.to_dict(),
            'nominee': nom.nominee,
            'didWin': False,
            'votes': nom.votes
        })

    return jsonify(result)