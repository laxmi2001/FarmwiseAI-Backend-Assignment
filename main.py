from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
import sqlite3
from flask_jwt_extended import JWTManager, jwt_required, create_access_token

conn = sqlite3.connect('instance/books.db')

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///books.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = 'my_secret_key'

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)


jwt = JWTManager(app)

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    isbn = db.Column(db.String(13), unique=True, nullable=False)
    price = db.Column(db.Float, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


with app.app_context():
    db.create_all()


@app.route('/books', methods=['POST'])
@jwt_required()
def add_book():
    data = request.get_json()
    new_book = Book(title=data['title'], author=data['author'], isbn=data['isbn'], price=data['price'],
                    quantity=data['quantity'])
    db.session.add(new_book)
    db.session.commit()
    return jsonify({'message': 'Book added successfully'})


@app.route('/books', methods=['GET'])
@jwt_required()
def get_all_books():
    books = Book.query.all()
    result = []
    for book in books:
        book_data = {'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price,
                     'quantity': book.quantity}
        result.append(book_data)
    return jsonify(result)


@app.route('/books/<isbn>', methods=['GET'])
@jwt_required()
def get_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        book_data = {'title': book.title, 'author': book.author, 'isbn': book.isbn, 'price': book.price,
                     'quantity': book.quantity}
        return jsonify(book_data)
    return jsonify({'message': 'Book not found'})


@app.route('/books/<isbn>', methods=['PUT'])
@jwt_required()
def update_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        data = request.get_json()
        book.title = data['title']
        book.author = data['author']
        book.price = data['price']
        book.quantity = data['quantity']
        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    return jsonify({'message': 'Book not found'})


@app.route('/books/<isbn>', methods=['DELETE'])
@jwt_required()
def delete_book(isbn):
    book = Book.query.filter_by(isbn=isbn).first()
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    return jsonify({'message': 'Book not found'})
