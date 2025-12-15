"""
Book routes for Library Management API
Provides REST endpoints for book operations
"""

from flask import Blueprint, request, jsonify

books_bp = Blueprint('books', __name__)

# Global adapter instance (will be set by app.py)
book_adapter = None


def init_book_routes(adapter):
    """Initialize book routes with adapter instance"""
    global book_adapter
    book_adapter = adapter


@books_bp.route('/api/books', methods=['GET'])
def get_books():
    """Get all books"""
    try:
        # Create fresh cursor for this request
        conn = book_adapter.db.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT b.id, b.title, b.isbn, b.year, b.genre, b.copies, b.author_id, a.name AS author_name
            FROM Books b
            LEFT JOIN Authors a ON b.author_id = a.id
            ORDER BY b.title
        """)
        rows = cursor.fetchall()
        cursor.close()

        books = []
        for row in rows:
            books.append({
                'id': row[0],
                'title': row[1],
                'isbn': row[2],
                'year': row[3],
                'genre': row[4],
                'copies': row[5],
                'author_id': row[6],
                'author_name': row[7]
            })

        return jsonify({
            'success': True,
            'data': books,
            'message': f'Retrieved {len(books)} books'
        }), 200
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'code': 500
        }), 500


@books_bp.route('/api/books/<int:book_id>', methods=['GET'])
def get_book(book_id):
    """Get book by ID"""
    try:
        book = book_adapter.get_by_id(book_id)
        if book:
            return jsonify({
                'success': True,
                'data': book,
                'message': 'Book retrieved successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Book with ID {book_id} not found',
                'code': 404
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@books_bp.route('/api/books', methods=['POST'])
def create_book():
    """Create new book"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'title' not in data or 'isbn' not in data:
            return jsonify({
                'success': False,
                'error': 'Title and ISBN are required',
                'code': 400
            }), 400

        # Extract fields
        title = data.get('title')
        isbn = data.get('isbn')
        year = data.get('year')
        genre = data.get('genre')
        copies = data.get('copies', 1)
        author_id = data.get('author_id')

        # Convert empty strings to None
        if year == '':
            year = None
        if genre == '':
            genre = None
        if author_id == '':
            author_id = None

        # Create book
        book = book_adapter.create(title, isbn, year, genre, copies, author_id)

        if book:
            return jsonify({
                'success': True,
                'data': book,
                'message': 'Book created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create book (possibly duplicate ISBN)',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@books_bp.route('/api/books/<int:book_id>', methods=['PUT'])
def update_book(book_id):
    """Update book"""
    try:
        data = request.get_json()

        if not data:
            return jsonify({
                'success': False,
                'error': 'No data provided',
                'code': 400
            }), 400

        # Extract fields (only include if present)
        update_fields = {}
        if 'title' in data and data['title']:
            update_fields['title'] = data['title']
        if 'isbn' in data and data['isbn']:
            update_fields['isbn'] = data['isbn']
        if 'year' in data:
            update_fields['year'] = data['year'] if data['year'] != '' else None
        if 'genre' in data:
            update_fields['genre'] = data['genre'] if data['genre'] != '' else None
        if 'copies' in data:
            update_fields['copies'] = data['copies']
        if 'author_id' in data:
            update_fields['author_id'] = data['author_id'] if data['author_id'] != '' else None

        # Update book
        book = book_adapter.update(book_id, **update_fields)

        if book:
            return jsonify({
                'success': True,
                'data': book,
                'message': 'Book updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to update book (book may not exist or ISBN conflict)',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@books_bp.route('/api/books/<int:book_id>', methods=['DELETE'])
def delete_book(book_id):
    """Delete book"""
    try:
        success = book_adapter.delete(book_id)

        if success:
            return jsonify({
                'success': True,
                'message': f'Book {book_id} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to delete book (may not exist or has linked loans)',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@books_bp.route('/api/books/search', methods=['GET'])
def search_books():
    """Search books by query parameter"""
    try:
        query = request.args.get('q', '')

        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query parameter "q" is required',
                'code': 400
            }), 400

        books = book_adapter.search(query)

        return jsonify({
            'success': True,
            'data': books,
            'message': f'Found {len(books)} books matching "{query}"'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@books_bp.route('/api/books/count', methods=['GET'])
def get_books_count():
    """Get total book count"""
    try:
        count = book_adapter.get_count()

        return jsonify({
            'success': True,
            'data': {'count': count},
            'message': f'Total books: {count}'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500
