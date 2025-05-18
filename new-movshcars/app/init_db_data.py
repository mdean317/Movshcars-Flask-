from app.extensions import db
from app.models import Category

def init_db_data():
    if not Category.query.first():  
        print("Seeding categories...")
        categories = [
            Category(name='Best Picture'),
            Category(name='Best Director'),
            Category(name='Best Actor', isActing=True),
            Category(name='Best Actress', isActing=True),
            Category(name='Best Supporting Actor', isActing=True),
            Category(name='Best Supporting Actress', isActing=True),
            Category(name='Best Original Song', isSong=True),
            Category(name='Best Original Screenplay'),
            Category(name='Best Adapted Screenplay'),
            Category(name='Best Cinematography'),
            Category(name='Best Film Editing'),
            Category(name='Best Original Score'),
            Category(name='Best Production Design'),
            Category(name='Best Costume Design'),
            Category(name='Best Sound'),
            Category(name='Best Makeup and Hairstyling'),
            Category(name='Best Visual Effects'),
            Category(name='Best Short Film'),
        ]
        db.session.add_all(categories)
        db.session.commit()
    else:
        print("Categories already seeded.")

