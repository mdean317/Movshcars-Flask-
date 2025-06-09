from app.extensions import db
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin
from datetime import datetime, timezone

# Define db model; use UserMixin to indicate to flask_login packagethat this the authentication account
class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100))
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
    __table_args__ = (UniqueConstraint('username', name='username_uc'),
                     )

    # Define string presentation of model 
    def __repr__(self):
        return f'<User {self.user_id}>'
    
    # Function allowing us to use the user_id as the _id field for user model
    def get_id(self):
        return str(self.user_id)
    
    # Define dictionary conversion function
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }