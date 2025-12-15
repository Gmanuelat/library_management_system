"""
Book Manager module for Library Management System
Handles CRUD operations for books
"""

import sqlite3
from database import Database


class BookManager:
    """Manages book-related operations in the library system"""

    def __init__(self, database):
        """
        Initialize BookManager with database connection

        Args:
            database (Database): Database instance
        """
        self.db = database
        self.conn = database.get_connection()
        self.cursor = database.get_cursor()

    def add_book(self, title, isbn, year=None, genre=None, copies=1, author_id=None):
        """
        Add a new book to the database

        Args:
            title (str): Book title
            isbn (str): ISBN (unique identifier)
            year (int, optional): Publication year
            genre (str, optional): Book genre
            copies (int, optional): Number of copies (default: 1)
            author_id (int, optional): ID of the author

        Returns:
            int: ID of the newly created book, or None if failed
        """
        try:
            # SQL INSERT statement with parameters to prevent SQL injection
            query = """
                INSERT INTO Books (title, isbn, year, genre, copies, author_id)
                VALUES (?, ?, ?, ?, ?, ?)
            """

            self.cursor.execute(query, (title, isbn, year, genre, copies, author_id))
            self.conn.commit()

            book_id = self.cursor.lastrowid
            print(f"✓ Book added successfully! (ID: {book_id})")
            print(f"  Title: {title}")
            print(f"  ISBN: {isbn}")
            if year:
                print(f"  Year: {year}")
            if genre:
                print(f"  Genre: {genre}")
            print(f"  Copies: {copies}")
            if author_id:
                print(f"  Author ID: {author_id}")

            return book_id

        except sqlite3.IntegrityError as e:
            if 'isbn' in str(e).lower():
                print(f"✗ ISBN constraint error: This ISBN already exists in the database")
            else:
                print(f"✗ Database integrity error: {e}")
            return None
        except sqlite3.Error as e:
            print(f"✗ Error adding book: {e}")
            return None

    def view_all_books(self):
        """
        Display all books in a formatted table with author names

        Returns:
            list: List of book tuples, or empty list if none found
        """
        try:
            query = """
                SELECT b.id, b.title, b.isbn, b.year, b.genre, b.copies, b.author_id, a.name AS author_name
                FROM Books b
                LEFT JOIN Authors a ON b.author_id = a.id
                ORDER BY b.title
            """
            self.cursor.execute(query)
            books = self.cursor.fetchall()

            if not books:
                print("\n📚 No books found in the database.")
                return []

            # Print formatted table header
            print("\n" + "=" * 110)
            print(f"{'ID':<5} {'Title':<30} {'Author':<25} {'ISBN':<15} {'Year':<6} {'Genre':<15} {'Copies':<7}")
            print("=" * 110)

            # Print each book row
            for book in books:
                book_id, title, isbn, year, genre, copies, author_id, author_name = book
                year_str = str(year) if year else "N/A"
                genre_str = genre if genre else "N/A"
                author_str = author_name if author_name else "N/A"

                # Truncate long titles and author names to fit columns
                title_display = title[:28] + ".." if len(title) > 30 else title
                author_display = author_str[:23] + ".." if len(author_str) > 25 else author_str

                print(f"{book_id:<5} {title_display:<30} {author_display:<25} {isbn:<15} {year_str:<6} {genre_str:<15} {copies:<7}")

            print("=" * 110)
            print(f"Total books: {len(books)}\n")

            return books

        except sqlite3.Error as e:
            print(f"✗ Error retrieving books: {e}")
            return []

    def search_book(self, search_term):
        """
        Search for books by title, ISBN, genre, or author name

        Args:
            search_term (str): Term to search for

        Returns:
            list: List of matching book tuples
        """
        try:
            # Using LIKE operator for pattern matching across multiple fields
            query = """
                SELECT b.id, b.title, b.isbn, b.year, b.genre, b.copies, b.author_id, a.name AS author_name
                FROM Books b
                LEFT JOIN Authors a ON b.author_id = a.id
                WHERE b.title LIKE ? OR b.isbn LIKE ? OR b.genre LIKE ? OR a.name LIKE ?
                ORDER BY b.title
            """

            # Add wildcards for partial matching
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern, search_pattern, search_pattern, search_pattern))
            books = self.cursor.fetchall()

            if not books:
                print(f"\n📚 No books found matching '{search_term}'")
                return []

            # Print formatted results
            print(f"\n🔍 Search results for '{search_term}':")
            print("=" * 110)
            print(f"{'ID':<5} {'Title':<30} {'Author':<25} {'ISBN':<15} {'Year':<6} {'Genre':<15} {'Copies':<7}")
            print("=" * 110)

            for book in books:
                book_id, title, isbn, year, genre, copies, author_id, author_name = book
                year_str = str(year) if year else "N/A"
                genre_str = genre if genre else "N/A"
                author_str = author_name if author_name else "N/A"

                # Truncate long titles and author names to fit columns
                title_display = title[:28] + ".." if len(title) > 30 else title
                author_display = author_str[:23] + ".." if len(author_str) > 25 else author_str

                print(f"{book_id:<5} {title_display:<30} {author_display:<25} {isbn:<15} {year_str:<6} {genre_str:<15} {copies:<7}")

            print("=" * 110)
            print(f"Found {len(books)} book(s)\n")

            return books

        except sqlite3.Error as e:
            print(f"✗ Error searching books: {e}")
            return []

    def get_book_by_id(self, book_id):
        """
        Retrieve a specific book by ID

        Args:
            book_id (int): The ID of the book to retrieve

        Returns:
            tuple: Book data or None if not found
        """
        try:
            query = """
                SELECT b.id, b.title, b.isbn, b.year, b.genre, b.copies, b.author_id, a.name AS author_name
                FROM Books b
                LEFT JOIN Authors a ON b.author_id = a.id
                WHERE b.id = ?
            """

            self.cursor.execute(query, (book_id,))
            book = self.cursor.fetchone()

            if not book:
                print(f"\n✗ No book found with ID: {book_id}")
                return None

            # Display book details
            book_id, title, isbn, year, genre, copies, author_id, author_name = book
            print(f"\n📖 Book Details (ID: {book_id})")
            print("=" * 50)
            print(f"Title:      {title}")
            print(f"ISBN:       {isbn}")
            print(f"Year:       {year if year else 'N/A'}")
            print(f"Genre:      {genre if genre else 'N/A'}")
            print(f"Copies:     {copies}")
            if author_name:
                print(f"Author:     {author_name} (ID: {author_id})")
            else:
                print(f"Author:     N/A")
            print("=" * 50 + "\n")

            return book

        except sqlite3.Error as e:
            print(f"✗ Error retrieving book: {e}")
            return None

    def update_book(self, book_id, title=None, isbn=None, year=None, genre=None, copies=None, author_id=None):
        """
        Update an existing book's information

        Args:
            book_id (int): ID of the book to update
            title (str, optional): New title
            isbn (str, optional): New ISBN
            year (int, optional): New publication year
            genre (str, optional): New genre
            copies (int, optional): New number of copies
            author_id (int, optional): New author ID

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First check if book exists
            if not self.get_book_by_id(book_id):
                return False

            # Build dynamic UPDATE query based on provided fields
            updates = []
            params = []

            if title is not None:
                updates.append("title = ?")
                params.append(title)
            if isbn is not None:
                updates.append("isbn = ?")
                params.append(isbn)
            if year is not None:
                updates.append("year = ?")
                params.append(year)
            if genre is not None:
                updates.append("genre = ?")
                params.append(genre)
            if copies is not None:
                updates.append("copies = ?")
                params.append(copies)
            if author_id is not None:
                updates.append("author_id = ?")
                params.append(author_id)

            if not updates:
                print("✗ No fields to update")
                return False

            query = f"UPDATE Books SET {', '.join(updates)} WHERE id = ?"
            params.append(book_id)

            self.cursor.execute(query, params)
            self.conn.commit()

            print(f"✓ Book {book_id} updated successfully!")
            return True

        except sqlite3.IntegrityError as e:
            if 'isbn' in str(e).lower():
                print(f"✗ ISBN constraint error: This ISBN already exists in the database")
            else:
                print(f"✗ Database integrity error: {e}")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error updating book: {e}")
            return False

    def delete_book(self, book_id):
        """
        Delete a book from the database

        Args:
            book_id (int): ID of the book to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if book exists
            if not self.get_book_by_id(book_id):
                return False

            query = "DELETE FROM Books WHERE id = ?"
            self.cursor.execute(query, (book_id,))
            self.conn.commit()

            print(f"✓ Book {book_id} deleted successfully!")
            return True

        except sqlite3.IntegrityError:
            print(f"✗ Cannot delete book: Loans are linked to this book")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error deleting book: {e}")
            return False

    def get_book_count(self):
        """
        Get the total number of books

        Returns:
            int: Number of books in the database
        """
        try:
            query = "SELECT COUNT(*) FROM Books"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ Error counting books: {e}")
            return 0


# Test the BookManager class
if __name__ == "__main__":
    print("=== Library Management System - Book Manager Test ===\n")

    # Initialize database
    db = Database()

    if not db.connect():
        print("Failed to connect to database!")
        exit(1)

    # Create tables if they don't exist
    db.create_tables()

    # Initialize BookManager
    book_mgr = BookManager(db)

    print("\n--- Test 1: Adding Books ---")
    # Add test books
    book_mgr.add_book("1984", "978-0451524935", 1949, "Fiction", 5, 2)
    book_mgr.add_book("Pride and Prejudice", "978-0141439518", 1813, "Romance", 3, 5)
    book_mgr.add_book("The Great Gatsby", "978-0743273565", 1925, "Fiction", 4)

    print("\n--- Test 2: View All Books ---")
    book_mgr.view_all_books()

    print("\n--- Test 3: Search for Books ---")
    book_mgr.search_book("1984")
    book_mgr.search_book("Fiction")

    print("\n--- Test 4: Get Book by ID ---")
    book_mgr.get_book_by_id(1)
    book_mgr.get_book_by_id(999)  # Non-existent ID

    print("\n--- Test 5: Update Book ---")
    book_mgr.update_book(1, copies=10)
    book_mgr.get_book_by_id(1)

    print("\n--- Test 6: Book Count ---")
    count = book_mgr.get_book_count()
    print(f"Total books in database: {count}")

    # Close database connection
    db.close()

    print("\n✓ Book Manager tests complete!")
