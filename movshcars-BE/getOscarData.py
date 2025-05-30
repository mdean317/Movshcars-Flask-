from main import app
from app.extensions import db
import csv

from app.models.movie import Movie
from app.models.category import Category
from app.models.nomination import Nomination
from app.models.userNomination import UserNomination

with app.app_context():
    
    failed_rows = []

    try:
          
        with open('oscars-data-for-db.csv', newline='', encoding='utf-8') as csvfile:
            reader = csv.DictReader(csvfile)

            for row in reader:

            
                catName = row['Category'].strip()
                filmTitle = row['Film'].strip()
                imdb_id = row['FilmId'].strip()
                nominees = row['Nominees'].strip()
                didWin = row['Winner'].strip()
                song = row['Song'].strip()
                year=int(row['Year'].strip())
                didWinBool = False

                print(year)
                movie = Movie.query.filter_by(imdb_id=imdb_id).first()
                if not movie:
                    movie = Movie(title=filmTitle, year=year, imdb_id=imdb_id, poster = None)
                    db.session.add(movie)
                
                print(movie)

                category = Category.query.filter_by(name=catName).first()
                if not category:
                    raise ValueError("No category match")

                print(category.category_id)
                newNomination = Nomination.query.filter_by(movie_id=imdb_id, year = movie.year, category_id = category.category_id, nominee = nominees).first()

                if not newNomination:

                    newNomination = Nomination (year = movie.year,
                                            category_id = category.category_id,
                                            movie_id = imdb_id,
                                            nominee = nominees,
                                            song = song)
                
                    db.session.add(newNomination)
                    db.session.flush()
                    print(newNomination)

                if didWin == 'TRUE':
                       didWinBool = True
                
                newUserNomination = UserNomination.query.filter_by(user_id = 4, nomination_id=newNomination.nomination_id).first()
                print(newUserNomination)

                if not newUserNomination:
                    newUserNomination = UserNomination(user_id = 4, nomination_id=newNomination.nomination_id, didWin=didWinBool)
                    print(newUserNomination)
                    db.session.add(newUserNomination)

                db.session.commit()

        print("Import complete.")

    except Exception as e:
        print(f"Error on row: {row} — {e}")
        row['error'] = str(e) 
        failed_rows.append(row)

    # Save failed rows to file
    if failed_rows:
        with open('failed_rows.csv', 'w', newline='', encoding='utf-8') as fail_file:
            fieldnames = failed_rows[0].keys()
            writer = csv.DictWriter(fail_file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(failed_rows)
        print(f"{len(failed_rows)} rows failed and were written to 'failed_rows.csv'")
