"""
Database module for Library Management System
Handles SQLite database connection and table creation
"""

import sqlite3
import os


class Database:
    """Manages SQLite database connections and schema creation"""

    def __init__(self, db_path='../data/library.db'):
        """
        Initialize Database instance

        Args:
            db_path (str): Path to the SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None

    def connect(self):
        """
        Establish connection to the SQLite database
        Creates the database file if it doesn't exist
        """
        try:
            # Get the directory of this file
            current_dir = os.path.dirname(os.path.abspath(__file__))
            # Build the full path to the database
            full_db_path = os.path.join(current_dir, self.db_path)

            # Allow SQLite to be used across threads (for Flask)
            self.conn = sqlite3.connect(full_db_path, check_same_thread=False)
            self.cursor = self.conn.cursor()

            # Enable foreign key constraints
            self.cursor.execute("PRAGMA foreign_keys = ON")

            print(f"✓ Connected to database: {full_db_path}")
            return True
        except sqlite3.Error as e:
            print(f"✗ Error connecting to database: {e}")
            return False

    def create_tables(self):
        """
        Create all required tables for the library management system
        Tables: Authors, Books, Members, Loans
        """
        try:
            # Create Authors table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Authors (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    birth_year INTEGER,
                    nationality TEXT
                )
            """)

            # Create Books table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Books (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    isbn TEXT UNIQUE NOT NULL,
                    year INTEGER,
                    genre TEXT,
                    copies INTEGER DEFAULT 1,
                    author_id INTEGER,
                    FOREIGN KEY(author_id) REFERENCES Authors(id)
                )
            """)

            # Create Members table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Members (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    phone TEXT,
                    membership_date TEXT DEFAULT CURRENT_DATE,
                    status TEXT DEFAULT 'active'
                )
            """)

            # Create Loans table
            self.cursor.execute("""
                CREATE TABLE IF NOT EXISTS Loans (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    book_id INTEGER NOT NULL,
                    member_id INTEGER NOT NULL,
                    loan_date TEXT DEFAULT CURRENT_DATE,
                    due_date TEXT NOT NULL,
                    return_date TEXT,
                    status TEXT DEFAULT 'borrowed',
                    FOREIGN KEY(book_id) REFERENCES Books(id),
                    FOREIGN KEY(member_id) REFERENCES Members(id)
                )
            """)

            # Commit the changes
            self.conn.commit()

            print("✓ All tables created successfully!")
            print("  - Authors")
            print("  - Books")
            print("  - Members")
            print("  - Loans")
            return True

        except sqlite3.Error as e:
            print(f"✗ Error creating tables: {e}")
            return False

    def close(self):
        """
        Safely close the database connection
        """
        if self.conn:
            self.conn.close()
            print("✓ Database connection closed")

    def get_connection(self):
        """
        Return the database connection object

        Returns:
            sqlite3.Connection: Active database connection
        """
        return self.conn

    def get_cursor(self):
        """
        Return the database cursor object

        Returns:
            sqlite3.Cursor: Active database cursor
        """
        return self.cursor


# Test the database setup
if __name__ == "__main__":
    print("=== Library Management System - Database Setup ===\n")

    # Create database instance
    db = Database()

    # Connect to database
    if db.connect():
        # Create tables
        db.create_tables()

        # Verify tables were created
        db.cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type='table'
            ORDER BY name
        """)

        tables = db.cursor.fetchall()
        print("\n✓ Database verification:")
        print(f"  Total tables created: {len(tables)}")
        for table in tables:
            print(f"    - {table[0]}")

        # Close connection
        db.close()

        print("\n✓ Database setup complete!")
    else:
        print("\n✗ Database setup failed!")
