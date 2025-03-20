from flask import Blueprint, render_template, request
from . import db

views = Blueprint('views', __name__)

@views.route('/')
def home():
    cursor = db.cursor()
    cursor.execute("SELECT * FROM Books LIMIT 6")
    result = cursor.fetchall()
    cursor.close()
    return render_template("home.html", books = result)

@views.route("/books", methods=['GET', 'POST'])
def books():
    cursor = db.cursor()
    cursor.execute("SELECT genre, count(*) FROM Books GROUP BY genre")
    genres_result = cursor.fetchall()
    genres = request.form.getlist("genres")
    keywords = request.form.get("keywords")
    genre_str = "', '".join(genres)
    stars = request.form.getlist("star")
    if request.method == 'POST':
        if keywords != None:
            sql = "SELECT * FROM Books WHERE title LIKE %s "
            if len(genres) > 0:
                print(genres)
                end = "AND genre IN ('" + genre_str + "')"
                sql += end
            val = request.form.get("keywords")
            print(sql)
            print(genres)
            cursor.execute(sql, (('%' + val + '%',)))
        else:
            if len(genres) > 0:
                end = "WHERE genre IN ('" + "', '".join(genres) + "')"
            cursor.execute("SELECT * FROM Books " + end)
    else:
        genres = [row[0] for row in genres_result]
        cursor.execute("SELECT * FROM Books ")
    books_result = cursor.fetchall()
    cursor.close()
    print(genres)
    return render_template("books.html", books = books_result, genres = genres_result, checked_genres = genres, checked_stars = stars, keyword = keywords)