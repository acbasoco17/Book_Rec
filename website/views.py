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

@views.route("/book-info/<book_id>", defaults={'star_input': None})
@views.route("/book-info/<book_id>/<star_input>")
def book_info(book_id, star_input):
    cursor = db.cursor()
    user_stars = 0
    
    if 'user_id' in session:
        sql = "SELECT * FROM SurveyResults WHERE book_id = " + str(book_id) + " AND user_id = " + str(session['user_id'])
        cursor.execute(sql)
        user_rating = cursor.fetchone()
        
        if user_rating:
            user_stars = user_rating[3]
            if star_input:
                sql = "UPDATE SurveyResults SET rating = %s WHERE book_id = %s AND user_id = %s"
                val = (str(star_input), str(book_id), session['user_id'])
                user_stars = int(star_input)
        else:
            if star_input:
                sql = "INSERT INTO SurveyResults (user_id, book_id, rating) VALUES (%s, %s, %s)"
                val = (int(session['user_id']), int(book_id), int(star_input))
                user_stars = int(star_input)
            cursor.execute(sql, val)
            db.commit()

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
    print("user_stars:", user_stars)
    return render_template("book_info.html", book = book, ratings = avg, user_stars = user_stars)