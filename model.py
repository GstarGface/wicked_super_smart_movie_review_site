"""Models and database functions for Ratings project."""

from flask_sqlalchemy import SQLAlchemy
from correlation import pearson

# This is the connection to the SQLite database; we're getting this through
# the Flask-SQLAlchemy helper library. On this, we can find the `session`
# object, where we do most of our interactions (like committing, etc.)

db = SQLAlchemy()


##############################################################################
# Model definitions: Users/Movies/Ratings

class User(db.Model):
    """Users of movie ratings website"""

    __tablename__ = "users"

    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(64), nullable=True)
    password = db.Column(db.String(64), nullable=True)
    age = db.Column(db.Integer, nullable=True)
    zipcode = db.Column(db.String(15), nullable=True)

    def __repr__(self):
        """Provides helpful information when printed"""

        return "<User user_id = %s email = %s>" % (self.user_id, self.email)

    def similarity(self, other):
        """Return Pearson rating for user compared to other user."""

        u_ratings = {}
        paired_ratings = []

        for r in self.ratings:
            u_ratings[r.movie_id] = r

        for r in other.ratings:
            u_r = u_ratings.get(r.movie_id)
            if u_r:
                paired_ratings.append( (u_r.score, r.score) )

        if paired_ratings:
            return pearson(paired_ratings)

        else:
            return 0.0


    def predict_rating(self, movie):
        """Predict a user's rating of a movie."""

        other_ratings = movie.ratings
        other_users = [ r.user for r in other_ratings ]

        similarities = [
            (self.similarity(other_user), other_user)
            for other_user in other_users
        ]

        similarities.sort(reverse=True)
        sim, best_match_user = similarities[0]


        matched_rating = None
        for rating in other_ratings:
            if rating.user_id == best_match_user.user_id:
                return rating.score * sim

class Movie(db.Model):
    """Movies in the ratings website."""

    __tablename__="movies"

    movie_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    title = db.Column(db.String(64), nullable=False)
    released_at = db.Column(db.DateTime, nullable=True)
    imdb_url = db.Column(db.String(200), nullable=True)

    def __repr__(self):
        """Provides helpful information when printed"""

        return "<Movie movie_id = %s title = %s>" % (self.movie_id, self.title)

class Rating(db.Model):
    """Ratings for movies by users."""

    __tablename__="ratings"

    rating_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movies.movie_id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.user_id'), nullable=False)
    score = db.Column(db.Integer, nullable=False)

    # Defines relationship to User class
    user = db.relationship("User",
                            backref=db.backref("ratings", order_by=rating_id))

    # Defines relationship to Movie class
    movie = db.relationship("Movie",
                            backref=db.backref("ratings", order_by=rating_id))

    def __repr__(self):
        """Provides helpful information when printed"""

        return "<Rating rating_id = %s movie_id = %s user_id = %s score = %s>" % (self.rating_id, self.movie_id, self.user_id, self.score)


##############################################################################
# Helper functions

def connect_to_db(app):
    """Connect the database to our Flask app."""

    # Configure to use our SQLite database
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ratings.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from server import app
    connect_to_db(app)
    print "Connected to DB."