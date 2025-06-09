
# Import global db object
from app.extensions import db

# Import event functions from sqlalchemey
from sqlalchemy import event

# Import all models 
from .category import Category
from .movie import Movie
from .nomination import Nomination
from .user import User
from .userNomination import UserNomination

# Add event listener on user nomination inserts
@event.listens_for(UserNomination, 'after_insert')
def increment_nom_count(mapper, connection, target):

    # Add vote to the bank nomination
    connection.execute(
        db.update(Nomination).
        where(Nomination.nomination_id == target.nomination_id).
        values(votes = Nomination.votes + 1)
    )

# Add event listener on user nomination deletes
@event.listens_for(UserNomination, 'after_delete')
def decrement_movie_count(mapper, connection, target):

    # Remove vote to the bank nomination
    connection.execute(
        db.update(Nomination).
        where(Nomination.nomination_id == target.nomination_id).
        values(votes=Nomination.votes - 1)
    )

# Make all models visible 
__all__ = ['Category', 'Movie', 'Nomination', 'User', 'UserNomination']