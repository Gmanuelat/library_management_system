"""
Simple demo showing how to use AuthorManager
"""

from database import Database
from author_manager import AuthorManager

# Step 1: Connect to database
db = Database()
db.connect()

# Step 2: Create AuthorManager instance
author_mgr = AuthorManager(db)

print("=== Author Manager Demo ===\n")

# Example 1: View all authors
print("1. Viewing all authors:")
author_mgr.view_all_authors()

# Example 2: Search for an author
print("\n2. Searching for 'Orwell':")
author_mgr.search_author("Orwell")

# Example 3: Get specific author by ID
print("\n3. Getting author with ID 4:")
author_mgr.get_author_by_id(4)

# Example 4: Add a new author
print("\n4. Adding a new author:")
new_id = author_mgr.add_author("Stephen King", 1947, "American")

# Example 5: View updated list
print("\n5. Updated author list:")
author_mgr.view_all_authors()

# Example 6: Count authors
print(f"\n6. Total authors: {author_mgr.get_author_count()}")

# Clean up
db.close()
