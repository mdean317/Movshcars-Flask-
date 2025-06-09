# Import dependecies 
from main import app
from app.extensions import db
from werkzeug.security import generate_password_hash
import uuid
import csv

# Import db models 
from app.models.movie import Movie
from app.models.category import Category
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination
from app.models.user import User


# Conenct to main app
with app.app_context():
        
    # Initiate failed rows array. 
    failed_rows = []

    try:
            
        # First will create a dummy user, to represent the official Oscar nominations. 
                    
        # Generate a random password.
        dummy_password = str(uuid.uuid4())

        # Create the new user, hashing password.
        dummy_user = User(email='N/A', username='AMPAS', password=generate_password_hash(dummy_password, method='pbkdf2:sha256'))

        # add the new user to the database
        db.session.add(dummy_user)

        # Flush creates a new user ID without committing. We will need the ID to create the related usernomination. 
        db.session.flush()

        # Open CSV file, defining encoding and how to parse newlines. 
        with open('oscars-data-for-db.csv', newline='', encoding='utf-8') as csvfile:
                
            # Turns file into dict array, by using the csv package reader, turning each row into a dict. 
            reader = csv.DictReader(csvfile)

            # Loop for each row
            for row in reader:

                # Parese each column into a variable, stripping white space
                catName = row['Category'].strip()
                filmTitle = row['Film'].strip()
                imdb_id = row['FilmId'].strip()
                nominees = row['Nominees'].strip()
                didWin = row['Winner'].strip()
                song = row['Song'].strip()                    
                year=int(row['Year'].strip())
                    
                didWinBool = False
                if didWin == 'TRUE':
                    didWinBool = True
                    
                # Retrieve movie dict from db
                movie = Movie.query.filter_by(imdb_id=imdb_id).first()

                # If movie doesn't exist in db... 
                if not movie:

                    # ... create new movie dict,
                    movie = Movie(title=filmTitle, year=year, imdb_id=imdb_id, poster = None)
                    # and add it to db session. 
                    db.session.add(movie)
                    
                # Log movie for debugging
                print(movie)

                # Retrieve category dict from db
                category = Category.query.filter_by(name=catName).first()

                # If category doesn't exist in db... 
                if not category:
                        
                    # Raise error that category could not be matched 
                    raise ValueError("No category match")

                # Log category for debugging
                print(category.category_id)

                # Check if nominations already exists 
                newNomination = Nomination.query.filter_by(movie_id=imdb_id, year = movie.year, category_id = category.category_id, nominee = nominees).first()
                    
                # If it doesn't...
                if not newNomination:

                    # Create a new one
                    newNomination = Nomination (year = movie.year,
                                                category_id = category.category_id,
                                                movie_id = imdb_id,
                                                nominee = nominees,
                                                song = song)

                    # Add to session
                    db.session.add(newNomination)

                    # Flush creates a new nomination ID without committing. We will need the ID to create the related usernomination. 
                    db.session.flush()

                # Print for log/debug
                print(newNomination)

                # See if usernom exists 
                newUserNomination = UserNomination.query.filter_by(user_id = dummy_user.user_id, nomination_id=newNomination.nomination_id).first()
                    
                # Create new nominations
                if not newUserNomination:
                    newUserNomination = UserNomination(user_id = dummy_user.user_id, nomination_id=newNomination.nomination_id, didWin=didWinBool)
                    db.session.add(newUserNomination)

                # Print for log/debug
                print(newUserNomination)

                # Commit session
                db.session.commit()

        # Note for log/debugging 
        print("Import complete.")

    # Catch exceptions
    except Exception as e:

        # Log failed row
        print(f"Error on row: {row} — {e}")

        # Add error string to row dict
        row['error'] = str(e) 

        # Add row dict to failed rows array
        failed_rows.append(row)

    # After all rows and errors have been processed, save failed rows to a new file, if there are any
    if failed_rows:

        # Create new file in 'write' mode
        with open('failed_rows.csv', 'w', newline='', encoding='utf-8') as fail_file:

            # Gather fields from failed rows dict array into variable.
            fieldnames = failed_rows[0].keys() 

            # Creates a dict writer instance, using the failed row dict fields
            writer = csv.DictWriter(fail_file, fieldnames=fieldnames)

            # Write csv file header
            writer.writeheader()

            # Writer rows from array into file
            writer.writerows(failed_rows)
            
        # Log creation of the file with number of failed rows
        print(f"{len(failed_rows)} rows failed and were written to 'failed_rows.csv'")
