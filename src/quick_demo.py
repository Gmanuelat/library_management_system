"""
Quick demonstration of library management features
Shows what you can do with the system
"""

from database import Database
from book_manager import BookManager
from author_manager import AuthorManager

print("\n" + "=" * 60)
print("📚 LIBRARY MANAGEMENT SYSTEM - QUICK DEMO 📚".center(60))
print("=" * 60)

# Initialize
db = Database()
db.connect()
book_mgr = BookManager(db)
author_mgr = AuthorManager(db)

# Demo 1: View Authors
print("\n\n========== 1. VIEWING ALL AUTHORS ==========")
author_mgr.view_all_authors()

# Demo 2: View Books
print("\n\n========== 2. VIEWING ALL BOOKS ==========")
book_mgr.view_all_books()

# Demo 3: Search Books
print("\n\n========== 3. SEARCHING FOR FICTION BOOKS ==========")
book_mgr.search_book("Fiction")

# Demo 4: Get Specific Book
print("\n\n========== 4. GETTING BOOK DETAILS (ID: 1) ==========")
book_mgr.get_book_by_id(1)

# Demo 5: Statistics
print("\n\n========== 5. LIBRARY STATISTICS ==========")
print(f"📊 Total Authors: {author_mgr.get_author_count()}")
print(f"📊 Total Books: {book_mgr.get_book_count()}")

# Demo 6: Search by Author
print("\n\n========== 6. SEARCHING BOOKS BY AUTHOR 'ORWELL' ==========")
book_mgr.search_book("Orwell")

print("\n" + "=" * 60)
print("✓ Demo Complete!".center(60))
print("To use the interactive system, run: python3 library_cli.py".center(60))
print("=" * 60 + "\n")

db.close()
