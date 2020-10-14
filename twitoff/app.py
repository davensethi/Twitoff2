""" Main app/routing file for Twitoff"""

from flask import Flask, render_template
from .models import DB, User
from .twitter import insert_example_users
from os import getenv


## initalizing the app


def create_app ():
    """creates and configures flask application"""
    
    app = Flask(__name__)
    app.config['SQLAlCHEMY_DATABASE_URI'] = getenv('DATABASE_URI')
    app.config['SQLAlCHEMY_TRACK_MODIFCATIONS'] = False
    DB.init_app(app)

    @app.route('/')
    def root():
        return render_template("base.html", title="Home", users= User.query.all())
    
    @app.route('/update')
    def update():
        #adds our users
        insert_example_users()
        return render_template('base.html',title = "Home", users=User.query.all())
    
    @app.route('/reset')
    def reset():
    # resets datatbase
        DB.drop_all()
        DB.create_all()
        return render_template('base.html', titel='Home')
        
    
    return app