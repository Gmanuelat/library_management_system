"""
Author routes for Library Management API
Provides REST endpoints for author operations
"""

from flask import Blueprint, request, jsonify

authors_bp = Blueprint('authors', __name__)

# Global adapter instance (will be set by app.py)
author_adapter = None


def init_author_routes(adapter):
    """Initialize author routes with adapter instance"""
    global author_adapter
    author_adapter = adapter


@authors_bp.route('/api/authors', methods=['GET'])
def get_authors():
    """Get all authors"""
    try:
        # Create fresh cursor for this request
        conn = author_adapter.db.conn
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, name, birth_year, nationality
            FROM Authors
            ORDER BY name
        """)
        rows = cursor.fetchall()
        cursor.close()

        authors = []
        for row in rows:
            authors.append({
                'id': row[0],
                'name': row[1],
                'birth_year': row[2],
                'nationality': row[3]
            })

        return jsonify({
            'success': True,
            'data': authors,
            'message': f'Retrieved {len(authors)} authors'
        }), 200
    except Exception as e:
        import traceback
        return jsonify({
            'success': False,
            'error': str(e),
            'traceback': traceback.format_exc(),
            'code': 500
        }), 500


@authors_bp.route('/api/authors/<int:author_id>', methods=['GET'])
def get_author(author_id):
    """Get author by ID"""
    try:
        author = author_adapter.get_by_id(author_id)
        if author:
            return jsonify({
                'success': True,
                'data': author,
                'message': 'Author retrieved successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Author with ID {author_id} not found',
                'code': 404
            }), 404
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@authors_bp.route('/api/authors', methods=['POST'])
def create_author():
    """Create new author"""
    try:
        data = request.get_json()

        # Validate required fields
        if not data or 'name' not in data:
            return jsonify({
                'success': False,
                'error': 'Name is required',
                'code': 400
            }), 400

        # Extract fields
        name = data.get('name')
        birth_year = data.get('birth_year')
        nationality = data.get('nationality')

        # Convert empty strings to None
        if birth_year == '':
            birth_year = None
        if nationality == '':
            nationality = None

        # Create author
        author = author_adapter.create(name, birth_year, nationality)

        if author:
            return jsonify({
                'success': True,
                'data': author,
                'message': 'Author created successfully'
            }), 201
        else:
            return jsonify({
                'success': False,
                'error': 'Failed to create author',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@authors_bp.route('/api/authors/<int:author_id>', methods=['PUT'])
def update_author(author_id):
    """Update author"""
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
        if 'name' in data and data['name']:
            update_fields['name'] = data['name']
        if 'birth_year' in data:
            update_fields['birth_year'] = data['birth_year'] if data['birth_year'] != '' else None
        if 'nationality' in data:
            update_fields['nationality'] = data['nationality'] if data['nationality'] != '' else None

        # Update author
        author = author_adapter.update(author_id, **update_fields)

        if author:
            return jsonify({
                'success': True,
                'data': author,
                'message': 'Author updated successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to update author (author may not exist)',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@authors_bp.route('/api/authors/<int:author_id>', methods=['DELETE'])
def delete_author(author_id):
    """Delete author"""
    try:
        success = author_adapter.delete(author_id)

        if success:
            return jsonify({
                'success': True,
                'message': f'Author {author_id} deleted successfully'
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': f'Failed to delete author (may not exist or has linked books)',
                'code': 400
            }), 400

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@authors_bp.route('/api/authors/search', methods=['GET'])
def search_authors():
    """Search authors by query parameter"""
    try:
        query = request.args.get('q', '')

        if not query:
            return jsonify({
                'success': False,
                'error': 'Search query parameter "q" is required',
                'code': 400
            }), 400

        authors = author_adapter.search(query)

        return jsonify({
            'success': True,
            'data': authors,
            'message': f'Found {len(authors)} authors matching "{query}"'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500


@authors_bp.route('/api/authors/count', methods=['GET'])
def get_authors_count():
    """Get total author count"""
    try:
        count = author_adapter.get_count()

        return jsonify({
            'success': True,
            'data': {'count': count},
            'message': f'Total authors: {count}'
        }), 200

    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'code': 500
        }), 500
