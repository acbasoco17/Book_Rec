from flask import Flask
from . import private

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = private.SECRET_KEY

    from .views import views

    app.register_blueprint(views, url_prefix = "/")

    return app