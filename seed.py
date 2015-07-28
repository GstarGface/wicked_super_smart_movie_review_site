"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import User, Rating, Movie, connect_to_db, db
from datetime import datetime
from server import app


def load_users(file_name):
    """Loads users from u.user into database."""

    raw_data = open(file_name)

    for line in raw_data:
        row = line.rstrip().split("|")
        user_id = row[0]
        age = row[1]
        zipcode = row[4]

        user = User(user_id=user_id, age=age, zipcode=zipcode)

        db.session.add(user)
    db.session.commit()



def load_movies(file_name):
    """Load movies from u.item into database."""

    raw_data = open(file_name)

    for line in raw_data:
        row = line.rstrip().split("|")
        movie_id = row[0]
        title = row[1][:-6] #clean to remove (date)
        if row[2] == "":
            released_at = None
        else:
            released_at = datetime.strptime(row[2], "%d-%b-%Y") #clean to return datetime object not string
        imdb_url = row[4]
        

        movie = Movie(movie_id=movie_id, title=title,
        released_at=released_at, imdb_url=imdb_url)

        db.session.add(movie)
    db.session.commit()


def load_ratings(file_name):
    """Load ratings from u.data into database."""

    raw_data = open(file_name)

    for line in raw_data:
        row = " ".join(line.split())
        better_row = row.split()
        movie_id = better_row[0]
        user_id = better_row[1] #aint no errors now! woot  
        score = better_row[2]
        

        rating = Rating(movie_id=movie_id, user_id=user_id, score=score)

        db.session.add(rating)
    db.session.commit()


if __name__ == "__main__":
    connect_to_db(app)

    load_users("seed_data/u.user")
    load_movies("seed_data/u.item")
    load_ratings("seed_data/u.data")
