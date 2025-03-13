from flask import Blueprint, render_template

auth = Blueprint('auth', __name__)

@auth.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

@auth.route('/register')
def register():
    return render_template("register.html")