from app.extensions import db
from sqlalchemy import event
from .category import Category
from .movie import Movie
from .nomination import Nomination
from .user import User
from .userNomination import UserNomination

@event.listens_for(UserNomination, 'after_insert')
def increment_nom_count(mapper, connection, target):
    connection.execute(
        db.update(Nomination).
        where(Nomination.nomination_id == target.nomination_id).
        values(votes = Nomination.votes + 1)
    )

@event.listens_for(UserNomination, 'after_delete')
def decrement_movie_count(mapper, connection, target):
    connection.execute(
        db.update(Nomination).
        where(Nomination.nomination_id == target.nomination_id).
        values(votes=Nomination.votes - 1)
    )
    
__all__ = ['Category', 'Movie', 'Nomination', 'User', 'UserNomination']