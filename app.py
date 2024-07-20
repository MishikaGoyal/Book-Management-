from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.bookstore

@app.route('/')
def index():
    books = db.books.find()
    return render_template('index.html', books=books)

@app.route('/add', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'genre': request.form['genre'],
            'year': request.form['year']
        }
        db.books.insert_one(book)
        return redirect(url_for('index'))
    return render_template('add_book.html')

@app.route('/update/<id>', methods=['GET', 'POST'])
def update_book(id):
    book = db.books.find_one({'_id': ObjectId(id)})
    if request.method == 'POST':
        updated_book = {
            'title': request.form['title'],
            'author': request.form['author'],
            'genre': request.form['genre'],
            'year': request.form['year']
        }
        db.books.update_one({'_id': ObjectId(id)}, {"$set": updated_book})
        return redirect(url_for('index'))
    return render_template('update_book.html', book=book)

@app.route('/delete/<id>')
def delete_book(id):
    db.books.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/view')
def view_books():
    books = db.books.find()
    return render_template('view_books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
