from app.extensions import db
from sqlalchemy import UniqueConstraint
from datetime import datetime, timezone

# Define db model 
class Movie(db.Model):
    __tablename__ = 'movies'
    title = db.Column(db.String(80), nullable=False)
    year = db.Column(db.Integer, nullable=False)
    imdb_id = db.Column(db.String(80), nullable=True, primary_key=True)
    poster = db.Column(db.String(80), nullable=True)
    created_at = db.Column(
        db.DateTime, 
        default=datetime.now(timezone.utc),  
        nullable=False
    )
    updated_at = db.Column(
        db.DateTime, 
        default=datetime.now(timezone.utc),  
        onupdate=datetime.now(timezone.utc),  
        nullable=False
    )

    # Add constraint to prevent duplicate movies
    __table_args__ = (UniqueConstraint('title', 'year', name='_movie_year_uc'),
                     )

    # Define string presentation of model 
    def __repr__(self):
        return f'<Movie {self.title}>'
    
    # Define dictionary conversion function
    def to_dict(self):
        return {
            'title': self.title,
            'year': self.year,
            'imdb_id': self.imdb_id,
            'poster': self.poster
        }