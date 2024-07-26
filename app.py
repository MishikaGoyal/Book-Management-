from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId

app = Flask(__name__)
client = MongoClient('mongodb://localhost:27017/')
db = client.bookstore
books_collection = db['books']

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

@app.route('/view_books', methods=['GET'])
def view_books():
    search_query = request.args.get('search')
    page = int(request.args.get('page', 1))
    per_page = 10

    if search_query:
        books = books_collection.find({
            '$or': [
                {'title': {'$regex': search_query, '$options': 'i'}},
                {'author': {'$regex': search_query, '$options': 'i'}},
                {'genre': {'$regex': search_query, '$options': 'i'}},
                {'year': {'$regex': search_query, '$options': 'i'}}
            ]
        }).skip((page - 1) * per_page).limit(per_page)
        total_books = books_collection.count_documents({
            '$or': [
                {'title': {'$regex': search_query, '$options': 'i'}},
                {'author': {'$regex': search_query, '$options': 'i'}},
                {'genre': {'$regex': search_query, '$options': 'i'}},
                {'year': {'$regex': search_query, '$options': 'i'}}
            ]
        })
    else:
        books = books_collection.find().skip((page - 1) * per_page).limit(per_page)
        total_books = books_collection.count_documents({})

    total_pages = (total_books + per_page - 1) // per_page

    return render_template('view_books.html', books=books, page=page, total_pages=total_pages)


if __name__ == '__main__':
    app.run(debug=True)
