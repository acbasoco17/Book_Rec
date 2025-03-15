from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from . import db

auth = Blueprint('auth', __name__)

@auth.route('/sign_in')
def sign_in():
    return render_template("sign_in.html")

@auth.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        # TODO: Salt password
        password = request.form.get('password')
        password = generate_password_hash(password)

        cursor = db.cursor()
        # TODO: Finish
        sql = "SELECT * FROM Users WHERE email = %s"
        val = (email, )
        cursor.execute(sql, val)
        result = cursor.fetchall()
        if len(result) > 0:
            flash("User already exists.")
        else:
            # TODO: Finish
            sql = "INSERT INTO Users (username, password_hash, email) VALUES (%s, %s, %s)"
            val = (name, password, email)
            cursor.execute(sql, val)
            db.commit()
            cursor.close()
            session['user_email'] = email
            session['user_name'] = name
            flash("Added New User")
            return redirect(url_for('views.home'))
    return render_template("register.html")