"""
Simple demo showing how to use BookManager
"""

from database import Database
from book_manager import BookManager
from author_manager import AuthorManager

# Step 1: Connect to database
db = Database()
db.connect()

# Step 2: Create manager instances
book_mgr = BookManager(db)
author_mgr = AuthorManager(db)

print("=== Book Manager Demo ===\n")

# Example 1: View all books
print("1. Viewing all books:")
book_mgr.view_all_books()

# Example 2: Add new books
print("\n2. Adding new books:")
# Add books with author relationships
book_mgr.add_book("1984", "978-0451524935", 1949, "Fiction", 5, 2)
book_mgr.add_book("Pride and Prejudice", "978-0141439518", 1813, "Romance", 3, 5)
book_mgr.add_book("Norwegian Wood", "978-0375704024", 1987, "Fiction", 4, 4)

# Add book without author
book_mgr.add_book("The Great Gatsby", "978-0743273565", 1925, "Fiction", 2)

# Example 3: View updated list
print("\n3. Updated book list:")
book_mgr.view_all_books()

# Example 4: Search for books
print("\n4. Searching for books:")
print("\n   a) Search by title:")
book_mgr.search_book("1984")

print("\n   b) Search by genre:")
book_mgr.search_book("Fiction")

print("\n   c) Search by author name:")
book_mgr.search_book("Orwell")

# Example 5: Get specific book by ID
print("\n5. Getting book with ID 1:")
book_mgr.get_book_by_id(1)

# Example 6: Update book
print("\n6. Updating book (increasing copies):")
book_mgr.update_book(1, copies=10)
print("\n   Viewing updated book:")
book_mgr.get_book_by_id(1)

# Example 7: Count books
print(f"\n7. Total books: {book_mgr.get_book_count()}")

# Example 8: Final book list
print("\n8. Final book list:")
book_mgr.view_all_books()

# Clean up
db.close()
