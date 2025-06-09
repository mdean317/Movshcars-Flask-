from app.extensions import db

# Define db model 
class Category(db.Model):
    __tablename__ = 'categories'
    category_id = db.Column(db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    isActing = db.Column(db.Boolean, default=False, nullable=False)
    isSong = db.Column(db.Boolean, default=False, nullable=False)

    # Define string presentation of model 
    def __repr__(self):
        return f'<Category {self.name}>'
    
    # Define dictionary conversion function
    def to_dict(self):
        return {
            'category_id': self.category_id,
            'name': self.name,
            'isActing': self.isActing,
            'isSong': self.isSong
        }