from flask import Blueprint, request, jsonify
from app.models.movie import Movie
from app.extensions import db
import requests
from flask_cors import CORS

proxy = Blueprint('proxy', __name__, url_prefix='/api')
CORS(proxy)

@proxy.route('/<string:imdb_id>', methods=['POST'])
def updateMoviePoster(imdb_id):

    try:
        data = request.get_json()

        apiResponse = requests.post('https://graph.imdbapi.dev/v1', json=data)

        response_json = apiResponse.json()

        poster_url = (
            response_json.get("data", {})
            .get("title", {})
            .get("posters", [{}])[0]
            .get("url")
        )

        movie = Movie.query.get(imdb_id)

        if not movie:
            return jsonify({'error': 'Movie not found'}), 404

        movie.poster = data.get('poster', poster_url)
        db.session.commit()
        print('ADDED POSTER')
        print(Movie)

        return jsonify({'message': 'Movie updated successfully'})

    except Exception as error:
        db.session.rollback()
        return jsonify({'error': str(error)}), 500