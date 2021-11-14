import os
from .models import Book
from app import db, app
from flask import  request, jsonify


@app.route("/getall")
def get_all():
    try:
        # books=Book.query.all()
        #return  jsonify([e.serialize() for e in books])
        return  jsonify({'name':'El Quijote', 
                        'photo':'https://esefarad.com/wp-content/uploads/2016/02/don_quijote_y_sancho_panza.jpg',
                        'description':'Crazy Old Man'
        })
    except Exception as e:
	    return(str(e))

@app.route("/add", methods=['GET', 'POST'])
def add_book():
    name=request.args.get('name')
    photo=request.args.get('photo')
    description=request.args.get('descriptimport os')

@app.route("/get/<id_>")
def get_by_id(id_):
    try:
        book=Book.query.filter_by(id=id_).first()
        return jsonify(book.serialize())
    except Exception as e:
	    return(str(e))

@app.route("/add/form",methods=['GET', 'POST'])
def add_book_form():
    if request.method == 'POST':
        name=request.form.get('name')
        photo=request.form.get('photo')
        description=request.form.get('description')
        try:
            book=Book(
                name=name,
                photo=photo,
                description=description
            )
            db.session.add(book)
            db.session.commit()
            return "Book added. book id={}".format(book.id)
        except Exception as e:
            return(str(e))
    return render_template("getdata.html")