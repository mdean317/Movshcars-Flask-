from app.extensions import db
from sqlalchemy import UniqueConstraint
from flask_login import UserMixin

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    user_id = db.Column(db.Integer, nullable=False, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False, unique=True)
    password = db.Column(db.String(100))
    __table_args__ = (UniqueConstraint('username', name='username_uc'),
                     )

    def __repr__(self):
        return f'<User {self.user_id}>'
    
    def get_id(self):
        return str(self.user_id)
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'username': self.username,
            'email': self.email
        }