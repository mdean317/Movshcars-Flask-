from flask import Blueprint, request, jsonify
from app.extensions import db
from app.models.movie import Movie
from flask_cors import CORS

movies = Blueprint('movies', __name__, url_prefix='/movies')
CORS(movies)

@movies.route('/')
def home():
    return "Welcome"

@movies.route('/add', methods=['POST'])
def add_movie():
    try:
        data = request.get_json()
        new_movie = Movie(title=data['title'], year=data['year'])
        db.session.add(new_movie)
        db.session.commit()
        return jsonify({"message": "Movie added successfully"}), 201

    except Exception as error:
        db.session.rollback()
        return jsonify({"error": str(error)}), 500

@movies.route('/<int:year>')
def getMoviesByYear(year):

    print('in route')
    if year == 0: 
        print('getting all movies')
        moviesByYear = (db.session.query(Movie).order_by(Movie.title).all())

    else:
        moviesByYear = (db.session.query(Movie).filter(Movie.year == year).order_by(Movie.title).all())
    
    return jsonify([movie.to_dict() for movie in moviesByYear])

@movies.route('/fill/<int:year>')
def fillMorePosters(year):

    if (year == -1):

        moviesByYear = (db.session.query(Movie).all())

    else:

        moviesByYear = (db.session.query(Movie)
                    .filter(Movie.year == year)
                    .all()
                    )
        
    moviesByYear = (db.session.query(Movie).filter(Movie.poster.is_(None)).limit(100).all())

    return jsonify([movie.to_dict() for movie in moviesByYear])