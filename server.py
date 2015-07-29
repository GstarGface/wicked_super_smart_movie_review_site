"""Movie Ratings."""

from jinja2 import StrictUndefined

from flask import Flask, render_template, redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from model import User, Rating, Movie, connect_to_db, db


app = Flask(__name__)

# Required to use Flask sessions and the debug toolbar
app.secret_key = "ABC"

# Normally, if you use an undefined variable in Jinja2, it fails silently.
# This is horrible. Fix this so that, instead, it raises an error.
app.jinja_env.undefined = StrictUndefined


@app.route('/')
def index():
    """Homepage."""

    return render_template("homepage.html")

@app.route('/users')
def user_list():
    """Show list of all zee uzerz in zee database"""

    users = User.query.all()
    return render_template("user_list.html", users=users)


@app.route('/login', methods=["GET", "POST"])
def login():
    """A form to login to the movie site with your username and password"""
    if request.method == "GET":
        return render_template("login_form.html")

    else:
        username = request.form.get("username")
        password = request.form.get("password")

        session["username"] = username
        session["password"] = password

        flash("Thanks %s. You are now logged in!" % (session['username']))

        return redirect('/')
    
@app.route('/logout', methods=['GET', 'POST'])  
def logout():
    """ Logs the current user out. Clears the session."""

    del session["username"]
    del session["password"]

    flash("Logged Out")

    return redirect('/')     

if __name__ == "__main__":
    # We have to set debug=True here, since it has to be True at the point
    # that we invoke the DebugToolbarExtension
    app.debug = True

    connect_to_db(app)

    # Use the DebugToolbar
    DebugToolbarExtension(app)

    app.run()