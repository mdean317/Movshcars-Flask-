from flask import Blueprint, request, jsonify
from app.models.movie import Movie
from app.extensions import db
import requests
from flask_cors import CORS

# This was creating in an attempt tp use the API. Double check if necessary

# Initiate bluprint
proxy = Blueprint('proxy', __name__, url_prefix='/api')

# Apply CORS to blueprint
CORS(proxy)

# Logic tup update a movie poster in the db
@proxy.route('/<string:imdb_id>', methods=['POST'])
def updateMoviePoster(imdb_id):

    try:    

        # Parse the request data
        # CHECK WHAT IS IN THIS REQUEST
        data = request.get_json()
        
        # Request poster data from API
        apiResponse = requests.post('https://graph.imdbapi.dev/v1', json=data)
        
         # Parse API reply
        response_json = apiResponse.json()

        # Get only the poster URL from the parsed reply
        poster_url = (
            response_json.get("data", {})
            .get("title", {})
            .get("posters", [{}])[0]
            .get("url")
        )
        
        # Get movie dict from db based on movie identifier
        movie = Movie.query.get(imdb_id)

        # Make sure that movie exists
        if not movie:
            return jsonify({'error': 'Movie not found'}), 404

        # Update poster in movie dict
        # WHAT EXACTLY DOES DATA.GET DO? 
        movie.poster = data.get('poster', poster_url)

        # Commit to DB
        db.session.commit()
        
        # Return successful message
        return jsonify({'message': 'Movie updated successfully'})

    # Catch exception
    except Exception as error:
        
        # Rollback db session 
        db.session.rollback()

        # Return error message
        return jsonify({'error': str(error)}), 500