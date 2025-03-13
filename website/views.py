from flask import Blueprint, render_template
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Books LIMIT 6")
    result = cursor.fetchall()
    for i in result:
        print(i[2])
    return render_template("home.html", books = result)