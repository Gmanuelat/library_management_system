"""
API Adapters for Library Management System
Wraps BookManager and AuthorManager to provide JSON-friendly responses
"""

import io
import sys
import contextlib
from book_manager import BookManager
from author_manager import AuthorManager


class BookAPIAdapter:
    """Adapter to convert BookManager console output to JSON-friendly data"""

    def __init__(self, database):
        """
        Initialize BookAPIAdapter with database connection

        Args:
            database (Database): Database instance
        """
        self.manager = BookManager(database)
        self.db = database

    @contextlib.contextmanager
    def _suppress_output(self):
        """Context manager to suppress print statements"""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            yield
        finally:
            sys.stdout = old_stdout

    def _row_to_dict(self, row):
        """
        Convert book row tuple to dictionary

        Args:
            row: Database row tuple

        Returns:
            dict: Book data as dictionary, or None if row is None
        """
        if not row:
            return None

        # From JOIN query: id, title, isbn, year, genre, copies, author_id, author_name
        if len(row) >= 8:
            return {
                'id': row[0],
                'title': row[1],
                'isbn': row[2],
                'year': row[3],
                'genre': row[4],
                'copies': row[5],
                'author_id': row[6],
                'author_name': row[7]
            }
        else:
            # Fallback for basic book data
            return {
                'id': row[0],
                'title': row[1],
                'isbn': row[2],
                'year': row[3] if len(row) > 3 else None,
                'genre': row[4] if len(row) > 4 else None,
                'copies': row[5] if len(row) > 5 else 1,
                'author_id': row[6] if len(row) > 6 else None
            }

    def get_all(self):
        """
        Get all books as list of dictionaries

        Returns:
            list: List of book dictionaries
        """
        with self._suppress_output():
            rows = self.manager.view_all_books()
        return [self._row_to_dict(row) for row in rows]

    def get_by_id(self, book_id):
        """
        Get single book by ID

        Args:
            book_id (int): Book ID

        Returns:
            dict: Book data or None if not found
        """
        with self._suppress_output():
            row = self.manager.get_book_by_id(book_id)
        return self._row_to_dict(row)

    def create(self, title, isbn, year=None, genre=None, copies=1, author_id=None):
        """
        Create new book

        Args:
            title (str): Book title
            isbn (str): ISBN
            year (int, optional): Publication year
            genre (str, optional): Genre
            copies (int, optional): Number of copies
            author_id (int, optional): Author ID

        Returns:
            dict: Created book data or None if failed
        """
        with self._suppress_output():
            book_id = self.manager.add_book(title, isbn, year, genre, copies, author_id)

        if book_id:
            return self.get_by_id(book_id)
        return None

    def update(self, book_id, title=None, isbn=None, year=None, genre=None, copies=None, author_id=None):
        """
        Update book

        Args:
            book_id (int): Book ID
            title (str, optional): New title
            isbn (str, optional): New ISBN
            year (int, optional): New year
            genre (str, optional): New genre
            copies (int, optional): New copies count
            author_id (int, optional): New author ID

        Returns:
            dict: Updated book data or None if failed
        """
        with self._suppress_output():
            success = self.manager.update_book(book_id, title, isbn, year, genre, copies, author_id)

        if success:
            return self.get_by_id(book_id)
        return None

    def delete(self, book_id):
        """
        Delete book

        Args:
            book_id (int): Book ID

        Returns:
            bool: True if successful, False otherwise
        """
        with self._suppress_output():
            return self.manager.delete_book(book_id)

    def search(self, search_term):
        """
        Search books

        Args:
            search_term (str): Search query

        Returns:
            list: List of matching book dictionaries
        """
        with self._suppress_output():
            rows = self.manager.search_book(search_term)
        return [self._row_to_dict(row) for row in rows]

    def get_count(self):
        """
        Get total book count

        Returns:
            int: Number of books
        """
        with self._suppress_output():
            return self.manager.get_book_count()


class AuthorAPIAdapter:
    """Adapter to convert AuthorManager console output to JSON-friendly data"""

    def __init__(self, database):
        """
        Initialize AuthorAPIAdapter with database connection

        Args:
            database (Database): Database instance
        """
        self.manager = AuthorManager(database)
        self.db = database

    @contextlib.contextmanager
    def _suppress_output(self):
        """Context manager to suppress print statements"""
        old_stdout = sys.stdout
        sys.stdout = io.StringIO()
        try:
            yield
        finally:
            sys.stdout = old_stdout

    def _row_to_dict(self, row):
        """
        Convert author row tuple to dictionary

        Args:
            row: Database row tuple

        Returns:
            dict: Author data as dictionary, or None if row is None
        """
        if not row:
            return None

        # Author row: id, name, birth_year, nationality
        return {
            'id': row[0],
            'name': row[1],
            'birth_year': row[2] if len(row) > 2 else None,
            'nationality': row[3] if len(row) > 3 else None
        }

    def get_all(self):
        """
        Get all authors as list of dictionaries

        Returns:
            list: List of author dictionaries
        """
        with self._suppress_output():
            rows = self.manager.view_all_authors()
        return [self._row_to_dict(row) for row in rows]

    def get_by_id(self, author_id):
        """
        Get single author by ID

        Args:
            author_id (int): Author ID

        Returns:
            dict: Author data or None if not found
        """
        with self._suppress_output():
            row = self.manager.get_author_by_id(author_id)
        return self._row_to_dict(row)

    def create(self, name, birth_year=None, nationality=None):
        """
        Create new author

        Args:
            name (str): Author name
            birth_year (int, optional): Birth year
            nationality (str, optional): Nationality

        Returns:
            dict: Created author data or None if failed
        """
        with self._suppress_output():
            author_id = self.manager.add_author(name, birth_year, nationality)

        if author_id:
            return self.get_by_id(author_id)
        return None

    def update(self, author_id, name=None, birth_year=None, nationality=None):
        """
        Update author

        Args:
            author_id (int): Author ID
            name (str, optional): New name
            birth_year (int, optional): New birth year
            nationality (str, optional): New nationality

        Returns:
            dict: Updated author data or None if failed
        """
        with self._suppress_output():
            success = self.manager.update_author(author_id, name, birth_year, nationality)

        if success:
            return self.get_by_id(author_id)
        return None

    def delete(self, author_id):
        """
        Delete author

        Args:
            author_id (int): Author ID

        Returns:
            bool: True if successful, False otherwise
        """
        with self._suppress_output():
            return self.manager.delete_author(author_id)

    def search(self, search_term):
        """
        Search authors

        Args:
            search_term (str): Search query

        Returns:
            list: List of matching author dictionaries
        """
        with self._suppress_output():
            rows = self.manager.search_author(search_term)
        return [self._row_to_dict(row) for row in rows]

    def get_count(self):
        """
        Get total author count

        Returns:
            int: Number of authors
        """
        with self._suppress_output():
            return self.manager.get_author_count()
