# Import dependecies 
from flask import Blueprint, request, jsonify
from app.extensions import db
from flask_cors import CORS

# Import db models 
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination
from app.models.movie import Movie
from app.models.category import Category
from app.models.user import User

# Initiate bluprint
nominations = Blueprint('nominations', __name__, url_prefix='/noms')

# Apply CORS to blueprint
CORS(nominations)

# Logic for ADD nomination to DB route 
@nominations.route('/add', methods=['POST'])
def addNomination():
    
    try:
        
        # parse the request data
        data = request.get_json()

        # Create new nomination dict, using variables from the request.
        newNomination = Nomination(year=data['year'], category_id=data['category_id'], movie_id=data['movie'], 
                                    nominee=data['nominee'])
        
        # Add new nomination to db
        db.session.add(newNomination)
        db.session.commit()        

        # Get user email from request
        email = data['email']

        # Get user dict from db by email
        user = User.query.filter_by(email=email).first()
      
        # Create UserNomination dict, combining new nominationd and user. 
        newUserNomination = UserNomination(user_id=user.user_id, nomination_id=newNomination.nomination_id, didWin=False)

       # Add new UserNomination to db
        db.session.add(newUserNomination)
        db.session.commit() 

        # Return successful message
        return jsonify({"message": "Nomination added successfully"}), 201
    
    # Catch exception
    except Exception as error:

        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500

# Probably most common function to use - getting nominations by year and category. 
@nominations.route('/')
def getNomsByYearAndCategory():

    try: 
        # Get year and cat variables from request
        req_year= request.args.get('year', type=int)
        req_category_id = request.args.get('category', type=int)

        # Get all nominations which meet the criteria
        nomBank = (db.session.query(Nomination)
                    .filter(Nomination.category_id == req_category_id, Nomination.year == req_year)
                    .all()
                    )

        # Initiate return array
        result = []

        # Loop to add each nomination and all it's info to return array
        for nom in nomBank:

            # For each nom, get their corrosponding movie and category db data
            movieObj = db.session.get(Movie, nom.movie_id)
            categoryObj = db.session.get(Category, nom.category_id)
            
            # Add nomination to return array
            result.append({

                'nomination_id': nom.nomination_id,
                'year': nom.year,
                'category': categoryObj.to_dict(),
                'movie': movieObj.to_dict(),
                'nominee': nom.nominee,
                'didWin': False,
                'votes': nom.votes
            })

        # Return array with query results
        return jsonify(result)
    
    # Catch exception
    except Exception as error:

        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500