# Import dependecies 
from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.movie import Movie
from flask_cors import CORS

# Initiate bluprint
movies = Blueprint('movies', __name__, url_prefix='/movies')

# Apply CORS to blueprint
CORS(movies)

# Logic for ADD movie to DB route 
@movies.route('/add', methods=['POST'])
def add_movie():

    try:

        # parse the request data
        data = request.get_json()

        # ADD LOGIC HERE

        # Create new movie dict, using variables from the request.
        new_movie = Movie(title=data['title'], year=data['year'])

        # Add movie to db
        db.session.add(new_movie)
        db.session.commit()

        # Return successful message
        return jsonify({"message": "Movie added successfully"}), 201

    # Catch exception
    except Exception as error:

        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({"error": str(error)}), 500

# Logic to GET movies by year
@movies.route('/<int:year>')
def getMoviesByYear(year):

    # THIS IS TO BE REMOVED TO OWN METHOD
    if year == 0: 
        print('getting all movies')
        moviesByYear = (db.session.query(Movie).order_by(Movie.title).all())

    else:
        
        #Get all movies from db by year
        moviesByYear = (db.session.query(Movie).filter(Movie.year == year).order_by(Movie.title).all())
    
    # Return all movies found
    return jsonify([movie.to_dict() for movie in moviesByYear])

# Logic to add posters to db
@movies.route('/fill/<int:year>')
def fillMorePosters(year):

    # Note: This is a method to run in the background to add more poster urls for movie in db.
    # It is the most efficient way to do so, but it is not part of the user experience, and once all
    # posters are added to db, will be removed. 

    # Get 100 movies who don't have a poster yet. 
    moviesByYear = (db.session.query(Movie).filter(Movie.poster.is_(None)).limit(100).all())

    # Returns movies that need posters to be added
    return jsonify([movie.to_dict() for movie in moviesByYear])