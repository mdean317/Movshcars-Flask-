from app.extensions import db
from sqlalchemy import UniqueConstraint

class Nomination(db.Model):
    __tablename__ = 'nominations'
    nomination_id = db.Column(db.Integer, nullable=False, primary_key=True)
    year = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('categories.category_id'), nullable=False) 
    movie_id = db.Column(db.String(80), db.ForeignKey('movies.imdb_id'), nullable=False) 
    nominee = db.Column(db.String(80), nullable=True)
    __table_args__ = (UniqueConstraint('year', 'category_id', 'movie_id', 'nominee', name='nominee_year_movie_category_uc'),
                     )
    
    def __repr__(self):
        return f'<Nomination {self.nomination_id}>'
    
    def to_dict(self):
        return {
            'year': self.year,
            'category_id': self.category_id,
            'movie_id': self.movie_id,
            'nominee': self.nominee,
        }