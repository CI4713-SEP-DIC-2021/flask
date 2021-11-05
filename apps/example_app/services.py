import os
from .models import Book
from app import db, app
from flask import request, jsonify


@app.route("/getall")
def get_all():
    try:
        books = Book.query.all()
        return jsonify([e.serialize() for e in books])
    except Exception as e:
        return str(e)


@app.route("/add")
def add_book():
    name = request.args.get("name")
    author = request.args.get("author")
    published = request.args.get("published")
    try:
        book = Book(name=name, author=author, published=published)
        db.session.add(book)
        db.session.commit()
        return "Book added. book id={}".format(book.id)
    except Exception as e:
        return str(e)


@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book = Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
        return str(e)


@app.route("/add/form", methods=["GET", "POST"])
def add_book_form():
    if request.method == "POST":
        name = request.form.get("name")
        author = request.form.get("author")
        published = request.form.get("published")
        try:
            book = Book(name=name, author=author, published=published)
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return str(e)
    return render_template("getdata.html")
