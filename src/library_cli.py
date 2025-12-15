"""
Interactive CLI for Library Management System
Provides a menu-driven interface for managing books and authors
"""

from database import Database
from book_manager import BookManager
from author_manager import AuthorManager


def print_header():
    """Print the application header"""
    print("\n" + "=" * 60)
    print("📚 LIBRARY MANAGEMENT SYSTEM 📚".center(60))
    print("=" * 60)


def print_menu():
    """Print the main menu"""
    print("\n--- MAIN MENU ---")
    print("1. Book Management")
    print("2. Author Management")
    print("3. Exit")
    print("-" * 30)


def print_book_menu():
    """Print the book management menu"""
    print("\n--- BOOK MANAGEMENT ---")
    print("1. View All Books")
    print("2. Search Books")
    print("3. Add New Book")
    print("4. Update Book")
    print("5. Delete Book")
    print("6. Get Book by ID")
    print("7. Book Count")
    print("8. Back to Main Menu")
    print("-" * 30)


def print_author_menu():
    """Print the author management menu"""
    print("\n--- AUTHOR MANAGEMENT ---")
    print("1. View All Authors")
    print("2. Search Authors")
    print("3. Add New Author")
    print("4. Update Author")
    print("5. Delete Author")
    print("6. Get Author by ID")
    print("7. Author Count")
    print("8. Back to Main Menu")
    print("-" * 30)


def get_input(prompt, required=True, input_type=str):
    """
    Get user input with validation

    Args:
        prompt (str): Prompt message
        required (bool): Whether input is required
        input_type (type): Expected type (str, int)

    Returns:
        User input converted to specified type, or None if not required and empty
    """
    while True:
        try:
            value = input(prompt).strip()

            if not value:
                if required:
                    print("✗ This field is required. Please try again.")
                    continue
                return None

            if input_type == int:
                return int(value)
            return value

        except ValueError:
            print(f"✗ Invalid input. Please enter a valid {input_type.__name__}.")


def handle_book_management(book_mgr, author_mgr):
    """Handle book management operations"""
    while True:
        print_book_menu()
        choice = get_input("Enter your choice (1-8): ", input_type=int)

        if choice == 1:
            # View All Books
            print("\n📚 Viewing All Books:")
            book_mgr.view_all_books()

        elif choice == 2:
            # Search Books
            search_term = get_input("Enter search term (title/ISBN/genre/author): ")
            book_mgr.search_book(search_term)

        elif choice == 3:
            # Add New Book
            print("\n--- Add New Book ---")
            title = get_input("Enter book title: ")
            isbn = get_input("Enter ISBN: ")
            year = get_input("Enter publication year (optional): ", required=False, input_type=int)
            genre = get_input("Enter genre (optional): ", required=False)
            copies = get_input("Enter number of copies (default 1): ", required=False, input_type=int)
            if copies is None:
                copies = 1

            # Ask if they want to link an author
            link_author = get_input("Link to an author? (y/n): ").lower()
            author_id = None
            if link_author == 'y':
                print("\nAvailable Authors:")
                author_mgr.view_all_authors()
                author_id = get_input("Enter Author ID (or leave blank): ", required=False, input_type=int)

            book_mgr.add_book(title, isbn, year, genre, copies, author_id)

        elif choice == 4:
            # Update Book
            print("\n--- Update Book ---")
            book_mgr.view_all_books()
            book_id = get_input("Enter Book ID to update: ", input_type=int)

            print("\nEnter new values (leave blank to keep current):")
            title = get_input("New title: ", required=False)
            isbn = get_input("New ISBN: ", required=False)
            year = get_input("New year: ", required=False, input_type=int)
            genre = get_input("New genre: ", required=False)
            copies = get_input("New number of copies: ", required=False, input_type=int)
            author_id = get_input("New author ID: ", required=False, input_type=int)

            book_mgr.update_book(book_id, title, isbn, year, genre, copies, author_id)

        elif choice == 5:
            # Delete Book
            print("\n--- Delete Book ---")
            book_mgr.view_all_books()
            book_id = get_input("Enter Book ID to delete: ", input_type=int)
            confirm = get_input(f"Are you sure you want to delete book {book_id}? (y/n): ").lower()
            if confirm == 'y':
                book_mgr.delete_book(book_id)
            else:
                print("✗ Deletion cancelled.")

        elif choice == 6:
            # Get Book by ID
            book_id = get_input("Enter Book ID: ", input_type=int)
            book_mgr.get_book_by_id(book_id)

        elif choice == 7:
            # Book Count
            count = book_mgr.get_book_count()
            print(f"\n📊 Total books in library: {count}")

        elif choice == 8:
            # Back to Main Menu
            break

        else:
            print("✗ Invalid choice. Please select 1-8.")


def handle_author_management(author_mgr):
    """Handle author management operations"""
    while True:
        print_author_menu()
        choice = get_input("Enter your choice (1-8): ", input_type=int)

        if choice == 1:
            # View All Authors
            print("\n📚 Viewing All Authors:")
            author_mgr.view_all_authors()

        elif choice == 2:
            # Search Authors
            search_term = get_input("Enter search term (name): ")
            author_mgr.search_author(search_term)

        elif choice == 3:
            # Add New Author
            print("\n--- Add New Author ---")
            name = get_input("Enter author name: ")
            birth_year = get_input("Enter birth year (optional): ", required=False, input_type=int)
            nationality = get_input("Enter nationality (optional): ", required=False)

            author_mgr.add_author(name, birth_year, nationality)

        elif choice == 4:
            # Update Author
            print("\n--- Update Author ---")
            author_mgr.view_all_authors()
            author_id = get_input("Enter Author ID to update: ", input_type=int)

            print("\nEnter new values (leave blank to keep current):")
            name = get_input("New name: ", required=False)
            birth_year = get_input("New birth year: ", required=False, input_type=int)
            nationality = get_input("New nationality: ", required=False)

            author_mgr.update_author(author_id, name, birth_year, nationality)

        elif choice == 5:
            # Delete Author
            print("\n--- Delete Author ---")
            author_mgr.view_all_authors()
            author_id = get_input("Enter Author ID to delete: ", input_type=int)
            confirm = get_input(f"Are you sure you want to delete author {author_id}? (y/n): ").lower()
            if confirm == 'y':
                author_mgr.delete_author(author_id)
            else:
                print("✗ Deletion cancelled.")

        elif choice == 6:
            # Get Author by ID
            author_id = get_input("Enter Author ID: ", input_type=int)
            author_mgr.get_author_by_id(author_id)

        elif choice == 7:
            # Author Count
            count = author_mgr.get_author_count()
            print(f"\n📊 Total authors in library: {count}")

        elif choice == 8:
            # Back to Main Menu
            break

        else:
            print("✗ Invalid choice. Please select 1-8.")


def main():
    """Main application entry point"""
    print_header()
    print("\n👋 Welcome to the Library Management System!")

    # Initialize database
    db = Database()
    if not db.connect():
        print("✗ Failed to connect to database. Exiting...")
        return

    # Create managers
    book_mgr = BookManager(db)
    author_mgr = AuthorManager(db)

    # Main loop
    while True:
        print_menu()
        choice = get_input("Enter your choice (1-3): ", input_type=int)

        if choice == 1:
            handle_book_management(book_mgr, author_mgr)

        elif choice == 2:
            handle_author_management(author_mgr)

        elif choice == 3:
            print("\n👋 Thank you for using the Library Management System!")
            print("📚 Closing database connection...")
            db.close()
            print("✓ Goodbye!\n")
            break

        else:
            print("✗ Invalid choice. Please select 1-3.")


if __name__ == "__main__":
    main()
