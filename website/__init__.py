from flask import Flask
from . import private
import mysql.connector

# TODO: Combine SurveyResults with Recommendations
# TODO: Add web address of images to database
db = mysql.connector.connect (
    host = "localhost",
    user = private.DB_USERNAME,
    password = private.DB_PASSWORD,
    database = "Look_A_Book"
)


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = private.SECRET_KEY
    app.config['SESSION_TYPE'] = "filesystem"

    from .views import views, book
    from.auth import auth

    app.register_blueprint(views, url_prefix = "/")
    app.register_blueprint(auth, url_prefix = "/")
    app.register_blueprint(book, url_prefix="/")

    return app