from app.extensions import db
from datetime import datetime
from datetime import datetime, timezone


class UserNomination(db.Model):
    __tablename__ = 'user_nominations'
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False, primary_key=True) 
    nomination_id = db.Column(db.Integer, db.ForeignKey('nominations.nomination_id'), nullable=False, primary_key=True) 
    didWin = db.Column(db.Boolean, default=False, nullable=False)
    '''
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
    '''
    def __repr__(self):
        return f'<UserNomination {self.user_id} nom: {self.nomination_id}>'
    
    def to_dict(self):
        return {
            'user_id': self.user_id,
            'nomination_id': self.nomination_id,
            'didWin': self.didWin
        }