from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path


db = SQLAlchemy()
DB_NAME = "kentofariki.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "kwnrujgnirjmeofrki"
    app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{DB_NAME}"
    db.init_app(app)

    from .models import User, User_info, User_price, Case, CSGO_Item

    create_database(app)

    print('loll')
    return app


def create_database(app):
    if not path.exists("website/" + DB_NAME):
        db.create_all(app=app)
        print("Created Database!")