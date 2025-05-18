from app.extensions import db
from sqlalchemy import UniqueConstraint

class Movie(db.Model):
    __tablename__ = 'movies'
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    imdb_id = db.Column(db.String(80), nullable=True, primary_key=True)
    poster = db.Column(db.String(80), nullable=True)
    __table_args__ = (UniqueConstraint('title', 'year', name='_movie_year_uc'),
                     )

    def __repr__(self):
        return f'<Movie {self.title}>'
    
    def to_dict(self):
        return {
            'title': self.title,
            'year': self.year,
            'imdb_id': self.imdb_id,
            'poster': self.poster
        }