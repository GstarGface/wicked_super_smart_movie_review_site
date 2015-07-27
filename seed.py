"""Utility file to seed ratings database from MovieLens data in seed_data/"""

from model import Users, Ratings, Movies, connect_to_db, db
from server import app


def load_users(file_name):
    """Loads users from u.user into database."""

    raw_data = open(file_name)

    for line in raw_data:
        row = line.rstrip().split("|")
        user_id = row[0]
        email = row[1]
        password = row[2]
        age = row[3]
        zipcode = row[4]

        user = Users(user_id=user_id, email=email,
        password=password, age=age, zipcode=zipcode)

        db.session.add(user)
        # db.session.commit()



def load_movies():
    """Load movies from u.item into database."""


def load_ratings():
    """Load ratings from u.data into database."""


if __name__ == "__main__":
    connect_to_db(app)

    load_users("u.users")
    load_movies()
    load_ratings()
