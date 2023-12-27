from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Book, book_schema, books_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/getdata')
def getdata():
    return {'yee': 'haw'}

@api.route('/book', methods = ['POST'])
@token_required
def create_book(current_user_token):
    author_name = request.json['author_name']
    book_title = request.json['book_title']
    book_len = request.json['book_len']
    isbn = request.json['isbn']
    user_token = current_user_token.token

    print(f'BIG TESTER: {current_user_token.token}')

    book = Book(author_name, book_title, book_len, isbn, user_token = user_token )

    db.session.add(book)
    db.session.commit()

    response = book_schema.dump(book)
    return jsonify(response)

@api.route('/books', methods = ['GET'])
@token_required
def get_books(current_user_token):
    a_user = current_user_token.token
    books = Book.query.filter_by(user_token = a_user).all()
    print(books)
    response = books_schema.dump(books)
    return jsonify(response)




@api.route('/books/<id>', methods=['POST', 'PUT'])
@token_required
def update_book(current_user_token, id):
    book = Book.query.get(id) 
    book.auth_name = request.json['auth_name']
    book.book_title = request.json['book_title']
    book.book_len = request.json['book_len'] 
    book.isbn=request.json['isbn']
    book.user_token = current_user_token.token

    db.session.commit()
    response = book_schema.dump(book)
    return jsonify(response)



@api.route('/books/<id>', methods=['DELETE'])
@token_required
def delete_book(current_user_token, id):
    book = Book.query.get(id)
    if book:
        db.session.delete(book)
        db.session.commit()
        return jsonify({'message': 'Book deleted successfully'})
    else:
        return jsonify({'message': 'Book not found'}), 404
