from flask import Blueprint, render_template, request, redirect, url_for, session
from . import db

views = Blueprint('views', __name__)
book = Blueprint('book', __name__)

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
    #TODO: Change this so the numbers change based off search results
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
    return render_template("books.html", books = books_result, genres = genres_result, checked_genres = genres, checked_stars = stars, keyword = keywords)

@views.route("/book-info/<book_id>")
def book_info(book_id):
    cursor = db.cursor()
    user_stars = 0
    if 'user_email' in session:
        sql = "SELECT * FROM SurveyResults WHERE user_id = " + str(session['user_id']) + " AND book_id = " + str(book_id)
        cursor.execute(sql)
        user_survey = cursor.fetchone()
        if user_survey:
            user_stars = user_survey[3]
    
    cursor.execute("SELECT * FROM Books WHERE book_id = %s", (str(book_id), ))
    book = cursor.fetchone()
    if not book:
        return redirect(url_for('views.books'))
    
    cursor.execute("SELECT * FROM SurveyResults WHERE book_id = %s", (str(book_id), ))
    surveys = cursor.fetchall()
    avg = 0
    if len(surveys) > 0:
        for i in surveys:
            avg += i[3]
        avg /= len(surveys)
    
    return render_template("book_info.html", book = book, ratings = avg, user_stars = user_stars)