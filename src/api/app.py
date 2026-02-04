"""
Flask Application for Library Management System
Main entry point for the web API
"""

import sys
import os

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from flask import Flask, send_from_directory, jsonify
from flask_cors import CORS
from database import Database
from api.adapters import BookAPIAdapter, AuthorAPIAdapter
from api.routes.books import books_bp, init_book_routes
from api.routes.authors import authors_bp, init_author_routes

# Initialize Flask app
app = Flask(__name__, static_folder='../static', static_url_path='/static')

# Enable CORS for API endpoints
CORS(app, resources={
    r"/api/*": {
        "origins": "*",
        "methods": ["GET", "POST", "PUT", "DELETE"],
        "allow_headers": ["Content-Type"]
    }
})

# Flask application context for database
from flask import g

def get_database():
    """Get database instance for current request"""
    if 'db' not in g:
        g.db = Database()
        if not g.db.connect():
            raise Exception("Failed to connect to database")
    return g.db

def get_book_adapter():
    """Get book adapter for current request"""
    if 'book_adapter' not in g:
        g.book_adapter = BookAPIAdapter(get_database())
    return g.book_adapter

def get_author_adapter():
    """Get author adapter for current request"""
    if 'author_adapter' not in g:
        g.author_adapter = AuthorAPIAdapter(get_database())
    return g.author_adapter

# Initialize adapters (create globals for routes to use)
try:
    # Create initial instances just for initialization
    temp_db = Database()
    temp_db.connect()
    book_adapter = BookAPIAdapter(temp_db)
    author_adapter = AuthorAPIAdapter(temp_db)

    # Initialize routes with adapters
    init_book_routes(book_adapter)
    init_author_routes(author_adapter)

    # Register blueprints
    app.register_blueprint(books_bp)
    app.register_blueprint(authors_bp)

except Exception as e:
    print(f"Error initializing application: {e}")
    sys.exit(1)


# Debug route
@app.route('/debug')
def debug():
    """Debug endpoint to check adapter functionality"""
    try:
        import os
        import sqlite3

        # Get database connection info
        db_conn_str = str(database.conn)

        # Try direct SQL query
        cursor = database.get_cursor()
        cursor.execute("SELECT COUNT(*) FROM Books")
        direct_book_count = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM Authors")
        direct_author_count = cursor.fetchone()[0]

        # Get database file path
        current_dir = os.path.dirname(os.path.abspath(__file__))
        resolved_db_path = os.path.join(current_dir, '..', '..', 'data', 'library.db')
        resolved_db_path = os.path.abspath(resolved_db_path)

        # Test through adapter
        books = book_adapter.get_all()
        authors = author_adapter.get_all()

        return jsonify({
            'db_connection': db_conn_str,
            'sql_book_count': direct_book_count,
            'sql_author_count': direct_author_count,
            'adapter_books_count': len(books),
            'adapter_authors_count': len(authors),
            'expected_db_path': resolved_db_path,
            'db_exists': os.path.exists(resolved_db_path),
            'sample_book': books[0] if books else None
        })
    except Exception as e:
        import traceback
        return jsonify({'error': str(e), 'traceback': traceback.format_exc()})

# Root route - serve index.html
@app.route('/')
def index():
    """Serve the main application page"""
    return send_from_directory(app.static_folder, 'index.html')


# Error handlers
@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return jsonify({
        'success': False,
        'error': 'Resource not found',
        'code': 404
    }), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return jsonify({
        'success': False,
        'error': 'Internal server error',
        'code': 500
    }), 500


@app.teardown_appcontext
def cleanup_database(exception=None):
    """Clean up database connection on app teardown"""
    db = g.pop('db', None)
    if db is not None:
        try:
            db.close()
        except:
            pass


if __name__ == '__main__':
    print("=" * 60)
    print("Library Management System - Web Interface".center(60))
    print("=" * 60)
    print("\nStarting Flask server...")
    print("Access the application at: http://localhost:5001")
    print("\nPress CTRL+C to stop the server\n")

    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)
