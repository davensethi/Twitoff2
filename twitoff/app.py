""" Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User


## initalizing the app


def create_app ():
    """creates and configures flask application"""
    
    app = Flask(__name__)
    app.config['SQLAlchemy_DATABASE_URI'] = "sqlite://db.sqlite3"
    app.config['SQLAlchemy_TRACK_MODIFCATIONS'] = False
    DB.init_app(app)

    #ToDO -- make rest of the application
    @app.route('/')
    def root():
        user = USer.query.all()
        return render_template("base.html", title="Home", users= User.query.all())
    
    return app