from flask import Flask, jsonify, abort, request, make_response

app = Flask(__name__)

# Mock Data
books = [
    {
        'book_id': 1,
        'title': "Where the Crawdads Sing",
        'author': "Delia Owens",
        'is_sold': False
    },
    {
        'book_id': 2,
        'title': "The Vanishing Half: A Novel",
        'author': "Brit Bennett",
        'is_sold': False
    },
    {
        'book_id': 3,
        'title': "1st Case",
        'author': "James Patterson, Chris Tebbetts",
        'is_sold': False
    }
]


@app.route('/')
def home():
    return "Welcome to Bhanu's Bookstore API Service"


@app.route('/books', methods=['GET'])
def get_books():
    return jsonify({'books': books})


@app.route('/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        abort(404)
    return jsonify({'book found': book})


@app.route('/books', methods=['POST'])
def add_book():
    if not request.json or not 'title' in request.json:
        abort(400)
    book = {
        'book_id': books[-1]['book_id'] + 1,  # just incrementing last book's ID for new book
        'title': request.json['title'],
        'author': request.json.get('author', ""),
        'is_sold': False
    }
    books.append(book)
    return jsonify({'newly added book': book}), 201


@app.route('/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    book = next((b for b in books if b['book_id'] == book_id), None)
    if not book:
        abort(404)
    if not request.json:
        abort(400)
    book['title'] = request.json.get('title', book['title'])
    book['author'] = request.json.get('author', book['author'])
    book['is_sold'] = request.json.get('is_sold', book['is_sold'])
    return jsonify({'updated book': book})


@app.route('/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    global books
    books = [book for book in books if book['book_id'] != book_id]
    return jsonify({'result': True})


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_request(error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
