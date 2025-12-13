"""
Author Manager module for Library Management System
Handles CRUD operations for authors
"""

import sqlite3
from database import Database


class AuthorManager:
    """Manages author-related operations in the library system"""

    def __init__(self, database):
        """
        Initialize AuthorManager with database connection

        Args:
            database (Database): Database instance
        """
        self.db = database
        self.conn = database.get_connection()
        self.cursor = database.get_cursor()

    def add_author(self, name, birth_year=None, nationality=None):
        """
        Add a new author to the database

        Args:
            name (str): Author's full name
            birth_year (int, optional): Year of birth
            nationality (str, optional): Author's nationality

        Returns:
            int: ID of the newly created author, or None if failed
        """
        try:
            # SQL INSERT statement with parameters to prevent SQL injection
            query = """
                INSERT INTO Authors (name, birth_year, nationality)
                VALUES (?, ?, ?)
            """

            self.cursor.execute(query, (name, birth_year, nationality))
            self.conn.commit()

            author_id = self.cursor.lastrowid
            print(f"✓ Author added successfully! (ID: {author_id})")
            print(f"  Name: {name}")
            if birth_year:
                print(f"  Birth Year: {birth_year}")
            if nationality:
                print(f"  Nationality: {nationality}")

            return author_id

        except sqlite3.IntegrityError as e:
            print(f"✗ Database integrity error: {e}")
            return None
        except sqlite3.Error as e:
            print(f"✗ Error adding author: {e}")
            return None

    def view_all_authors(self):
        """
        Display all authors in a formatted table

        Returns:
            list: List of author tuples, or empty list if none found
        """
        try:
            query = "SELECT id, name, birth_year, nationality FROM Authors ORDER BY name"
            self.cursor.execute(query)
            authors = self.cursor.fetchall()

            if not authors:
                print("\n📚 No authors found in the database.")
                return []

            # Print formatted table header
            print("\n" + "=" * 90)
            print(f"{'ID':<6} {'Name':<30} {'Birth Year':<12} {'Nationality':<30}")
            print("=" * 90)

            # Print each author row
            for author in authors:
                author_id, name, birth_year, nationality = author
                birth_year_str = str(birth_year) if birth_year else "N/A"
                nationality_str = nationality if nationality else "N/A"

                print(f"{author_id:<6} {name:<30} {birth_year_str:<12} {nationality_str:<30}")

            print("=" * 90)
            print(f"Total authors: {len(authors)}\n")

            return authors

        except sqlite3.Error as e:
            print(f"✗ Error retrieving authors: {e}")
            return []

    def search_author(self, search_term):
        """
        Search for authors by name using pattern matching

        Args:
            search_term (str): Name or partial name to search for

        Returns:
            list: List of matching author tuples
        """
        try:
            # Using LIKE operator for pattern matching (case-insensitive)
            query = """
                SELECT id, name, birth_year, nationality
                FROM Authors
                WHERE name LIKE ?
                ORDER BY name
            """

            # Add wildcards for partial matching
            search_pattern = f"%{search_term}%"
            self.cursor.execute(query, (search_pattern,))
            authors = self.cursor.fetchall()

            if not authors:
                print(f"\n📚 No authors found matching '{search_term}'")
                return []

            # Print formatted results
            print(f"\n🔍 Search results for '{search_term}':")
            print("=" * 90)
            print(f"{'ID':<6} {'Name':<30} {'Birth Year':<12} {'Nationality':<30}")
            print("=" * 90)

            for author in authors:
                author_id, name, birth_year, nationality = author
                birth_year_str = str(birth_year) if birth_year else "N/A"
                nationality_str = nationality if nationality else "N/A"

                print(f"{author_id:<6} {name:<30} {birth_year_str:<12} {nationality_str:<30}")

            print("=" * 90)
            print(f"Found {len(authors)} author(s)\n")

            return authors

        except sqlite3.Error as e:
            print(f"✗ Error searching authors: {e}")
            return []

    def get_author_by_id(self, author_id):
        """
        Retrieve a specific author by ID

        Args:
            author_id (int): The ID of the author to retrieve

        Returns:
            tuple: Author data (id, name, birth_year, nationality) or None if not found
        """
        try:
            query = """
                SELECT id, name, birth_year, nationality
                FROM Authors
                WHERE id = ?
            """

            self.cursor.execute(query, (author_id,))
            author = self.cursor.fetchone()

            if not author:
                print(f"\n✗ No author found with ID: {author_id}")
                return None

            # Display author details
            author_id, name, birth_year, nationality = author
            print(f"\n📖 Author Details (ID: {author_id})")
            print("=" * 50)
            print(f"Name:        {name}")
            print(f"Birth Year:  {birth_year if birth_year else 'N/A'}")
            print(f"Nationality: {nationality if nationality else 'N/A'}")
            print("=" * 50 + "\n")

            return author

        except sqlite3.Error as e:
            print(f"✗ Error retrieving author: {e}")
            return None

    def update_author(self, author_id, name=None, birth_year=None, nationality=None):
        """
        Update an existing author's information

        Args:
            author_id (int): ID of the author to update
            name (str, optional): New name
            birth_year (int, optional): New birth year
            nationality (str, optional): New nationality

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # First check if author exists
            if not self.get_author_by_id(author_id):
                return False

            # Build dynamic UPDATE query based on provided fields
            updates = []
            params = []

            if name is not None:
                updates.append("name = ?")
                params.append(name)
            if birth_year is not None:
                updates.append("birth_year = ?")
                params.append(birth_year)
            if nationality is not None:
                updates.append("nationality = ?")
                params.append(nationality)

            if not updates:
                print("✗ No fields to update")
                return False

            query = f"UPDATE Authors SET {', '.join(updates)} WHERE id = ?"
            params.append(author_id)

            self.cursor.execute(query, params)
            self.conn.commit()

            print(f"✓ Author {author_id} updated successfully!")
            return True

        except sqlite3.Error as e:
            print(f"✗ Error updating author: {e}")
            return False

    def delete_author(self, author_id):
        """
        Delete an author from the database

        Args:
            author_id (int): ID of the author to delete

        Returns:
            bool: True if successful, False otherwise
        """
        try:
            # Check if author exists
            if not self.get_author_by_id(author_id):
                return False

            query = "DELETE FROM Authors WHERE id = ?"
            self.cursor.execute(query, (author_id,))
            self.conn.commit()

            print(f"✓ Author {author_id} deleted successfully!")
            return True

        except sqlite3.IntegrityError:
            print(f"✗ Cannot delete author: Books are linked to this author")
            return False
        except sqlite3.Error as e:
            print(f"✗ Error deleting author: {e}")
            return False

    def get_author_count(self):
        """
        Get the total number of authors

        Returns:
            int: Number of authors in the database
        """
        try:
            query = "SELECT COUNT(*) FROM Authors"
            self.cursor.execute(query)
            count = self.cursor.fetchone()[0]
            return count
        except sqlite3.Error as e:
            print(f"✗ Error counting authors: {e}")
            return 0


# Test the AuthorManager class
if __name__ == "__main__":
    print("=== Library Management System - Author Manager Test ===\n")

    # Initialize database
    db = Database()

    if not db.connect():
        print("Failed to connect to database!")
        exit(1)

    # Create tables if they don't exist
    db.create_tables()

    # Initialize AuthorManager
    author_mgr = AuthorManager(db)

    print("\n--- Test 1: Adding Authors ---")
    # Add test authors
    author_mgr.add_author("J.K. Rowling", 1965, "British")
    author_mgr.add_author("George Orwell", 1903, "British")
    author_mgr.add_author("Gabriel García Márquez", 1927, "Colombian")
    author_mgr.add_author("Haruki Murakami", 1949, "Japanese")
    author_mgr.add_author("Jane Austen", 1775, "British")
    author_mgr.add_author("Leo Tolstoy", 1828, "Russian")
    author_mgr.add_author("Chimamanda Ngozi Adichie", 1977, "Nigerian")

    print("\n--- Test 2: View All Authors ---")
    author_mgr.view_all_authors()

    print("\n--- Test 3: Search for Authors ---")
    author_mgr.search_author("George")
    author_mgr.search_author("British")  # Search by nationality won't work with current query

    print("\n--- Test 4: Get Author by ID ---")
    author_mgr.get_author_by_id(1)
    author_mgr.get_author_by_id(999)  # Non-existent ID

    print("\n--- Test 5: Update Author ---")
    author_mgr.update_author(1, nationality="English")
    author_mgr.get_author_by_id(1)

    print("\n--- Test 6: Author Count ---")
    count = author_mgr.get_author_count()
    print(f"Total authors in database: {count}")

    # Close database connection
    db.close()

    print("\n✓ Author Manager tests complete!")
