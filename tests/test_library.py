"""
Playwright E2E tests for the Library Management System.
"""

import re
import pytest
from playwright.sync_api import expect


class TestPageLoad:
    """Tests for initial page load and structure."""

    def test_page_title(self, home_page):
        expect(home_page).to_have_title("Library Management System")

    def test_header_visible(self, home_page):
        header = home_page.locator("h1.logo")
        expect(header).to_have_text("Library Management System")

    def test_nav_tabs_visible(self, home_page):
        books_tab = home_page.locator("#nav-books")
        authors_tab = home_page.locator("#nav-authors")
        expect(books_tab).to_be_visible()
        expect(authors_tab).to_be_visible()

    def test_books_section_active_by_default(self, home_page):
        books_section = home_page.locator("#books-section")
        expect(books_section).to_have_class(re.compile(r"active"))

    def test_books_table_has_rows(self, home_page):
        rows = home_page.locator("#books-table-container table tbody tr")
        assert rows.count() > 0, "Books table should have at least one row"

    def test_books_table_headers(self, home_page):
        headers = home_page.locator("#books-table-container table thead th")
        expected = ["ID", "Title", "Author", "ISBN", "Year", "Genre", "Copies", "Actions"]
        for i, expected_text in enumerate(expected):
            expect(headers.nth(i)).to_have_text(expected_text)


class TestNavigation:
    """Tests for tab navigation between Books and Authors."""

    def test_switch_to_authors(self, home_page):
        home_page.locator("#nav-authors").click()

        authors_section = home_page.locator("#authors-section")
        expect(authors_section).to_have_class(re.compile(r"active"))

        books_section = home_page.locator("#books-section")
        expect(books_section).not_to_have_class(re.compile(r"active"))

    def test_switch_back_to_books(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.locator("#nav-books").click()

        books_section = home_page.locator("#books-section")
        expect(books_section).to_have_class(re.compile(r"active"))

    def test_authors_table_loads(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.wait_for_selector("#authors-table-container table", timeout=10000)

        rows = home_page.locator("#authors-table-container table tbody tr")
        assert rows.count() > 0, "Authors table should have at least one row"

    def test_authors_table_headers(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.wait_for_selector("#authors-table-container table", timeout=10000)

        headers = home_page.locator("#authors-table-container table thead th")
        expected = ["ID", "Name", "Birth Year", "Nationality", "Actions"]
        for i, expected_text in enumerate(expected):
            expect(headers.nth(i)).to_have_text(expected_text)


class TestBookSearch:
    """Tests for book search functionality."""

    def test_search_filters_results(self, home_page):
        search_input = home_page.locator("#books-search")
        search_input.fill("Pride")

        # Wait for debounced search (300ms) + network
        home_page.wait_for_timeout(1000)
        home_page.wait_for_selector("#books-table-container table", timeout=5000)

        rows = home_page.locator("#books-table-container table tbody tr")
        count = rows.count()
        assert count >= 1, "Search for 'Pride' should return at least one result"

        # Verify results contain the search term
        first_row_title = rows.first.locator("td").nth(1)
        expect(first_row_title).to_contain_text("Pride")

    def test_clear_search_shows_all(self, home_page):
        # Get initial count
        initial_rows = home_page.locator("#books-table-container table tbody tr")
        initial_count = initial_rows.count()

        # Search for something
        search_input = home_page.locator("#books-search")
        search_input.fill("Pride")
        home_page.wait_for_timeout(1000)

        # Clear search
        search_input.fill("")
        home_page.wait_for_timeout(1000)
        home_page.wait_for_selector("#books-table-container table", timeout=5000)

        rows = home_page.locator("#books-table-container table tbody tr")
        assert rows.count() == initial_count


class TestAuthorSearch:
    """Tests for author search functionality."""

    def test_author_search_filters_results(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.wait_for_selector("#authors-table-container table", timeout=10000)

        search_input = home_page.locator("#authors-search")
        search_input.fill("Mark")

        home_page.wait_for_timeout(1000)
        home_page.wait_for_selector("#authors-table-container table", timeout=5000)

        rows = home_page.locator("#authors-table-container table tbody tr")
        assert rows.count() >= 1, "Search for 'Mark' should return at least one result"


class TestAddBook:
    """Tests for adding a new book."""

    def test_add_book_modal_opens(self, home_page):
        home_page.locator("#add-book-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        modal_title = home_page.locator("#modal-body h2")
        expect(modal_title).to_have_text("Add New Book")

    def test_add_book_form_fields(self, home_page):
        home_page.locator("#add-book-btn").click()

        expect(home_page.locator("#book-title")).to_be_visible()
        expect(home_page.locator("#book-isbn")).to_be_visible()
        expect(home_page.locator("#book-year")).to_be_visible()
        expect(home_page.locator("#book-genre")).to_be_visible()
        expect(home_page.locator("#book-copies")).to_be_visible()
        expect(home_page.locator("#book-author")).to_be_visible()

    def test_add_book_cancel(self, home_page):
        home_page.locator("#add-book-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        home_page.locator("button:has-text('Cancel')").click()
        expect(modal).to_have_class(re.compile(r"hidden"))

    def test_add_book_submit(self, home_page):
        # Get initial row count
        initial_count = home_page.locator("#books-table-container table tbody tr").count()

        home_page.locator("#add-book-btn").click()

        # Fill out the form
        home_page.locator("#book-title").fill("Playwright Test Book")
        home_page.locator("#book-isbn").fill("TEST-ISBN-PW-001")
        home_page.locator("#book-year").fill("2024")
        home_page.locator("#book-genre").fill("Testing")
        home_page.locator("#book-copies").fill("3")

        # Submit
        home_page.locator("button:has-text('Add Book')").click()

        # Wait for modal to close and table to refresh
        modal = home_page.locator("#modal")
        expect(modal).to_have_class(re.compile(r"hidden"), timeout=5000)

        home_page.wait_for_selector("#books-table-container table", timeout=5000)

        # Verify toast notification
        toast = home_page.locator("#toast")
        expect(toast).to_contain_text("Book added successfully")

        # Verify the book appears in the table
        new_count = home_page.locator("#books-table-container table tbody tr").count()
        assert new_count == initial_count + 1


class TestAddAuthor:
    """Tests for adding a new author."""

    def test_add_author_modal_opens(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.wait_for_selector("#authors-table-container table", timeout=10000)

        home_page.locator("#add-author-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        modal_title = home_page.locator("#modal-body h2")
        expect(modal_title).to_have_text("Add New Author")

    def test_add_author_submit(self, home_page):
        home_page.locator("#nav-authors").click()
        home_page.wait_for_selector("#authors-table-container table", timeout=10000)

        initial_count = home_page.locator("#authors-table-container table tbody tr").count()

        home_page.locator("#add-author-btn").click()

        home_page.locator("#author-name").fill("Test Playwright Author")
        home_page.locator("#author-birth-year").fill("1990")
        home_page.locator("#author-nationality").fill("Testland")

        home_page.locator("button:has-text('Add Author')").click()

        modal = home_page.locator("#modal")
        expect(modal).to_have_class(re.compile(r"hidden"), timeout=5000)

        home_page.wait_for_selector("#authors-table-container table", timeout=5000)

        toast = home_page.locator("#toast")
        expect(toast).to_contain_text("Author added successfully")

        new_count = home_page.locator("#authors-table-container table tbody tr").count()
        assert new_count == initial_count + 1


class TestEditBook:
    """Tests for editing a book."""

    def test_edit_book_modal_opens(self, home_page):
        # Click the first Edit button in the books table
        edit_btn = home_page.locator("#books-table-container table tbody tr").first.locator(
            "button:has-text('Edit')"
        )
        edit_btn.click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        modal_title = home_page.locator("#modal-body h2")
        expect(modal_title).to_have_text("Edit Book")

    def test_edit_book_has_existing_values(self, home_page):
        # Get the title of the first book
        first_title = home_page.locator(
            "#books-table-container table tbody tr"
        ).first.locator("td").nth(1).inner_text()

        edit_btn = home_page.locator("#books-table-container table tbody tr").first.locator(
            "button:has-text('Edit')"
        )
        edit_btn.click()

        # Verify the title input is pre-filled
        title_input = home_page.locator("#book-title")
        expect(title_input).to_have_value(first_title)


class TestDeleteBook:
    """Tests for deleting a book."""

    def test_delete_book(self, home_page):
        # First add a book so we have something safe to delete
        home_page.locator("#add-book-btn").click()
        home_page.locator("#book-title").fill("Book To Delete")
        home_page.locator("#book-isbn").fill("DELETE-ME-ISBN-001")
        home_page.locator("button:has-text('Add Book')").click()

        modal = home_page.locator("#modal")
        expect(modal).to_have_class(re.compile(r"hidden"), timeout=5000)
        home_page.wait_for_selector("#books-table-container table", timeout=5000)
        home_page.wait_for_timeout(500)

        initial_count = home_page.locator("#books-table-container table tbody tr").count()

        # Accept the confirmation dialog
        home_page.on("dialog", lambda dialog: dialog.accept())

        # Click delete on the last row (our newly added book)
        delete_btn = home_page.locator("#books-table-container table tbody tr").last.locator(
            "button:has-text('Delete')"
        )
        delete_btn.click()

        # Wait for the table to refresh
        home_page.wait_for_timeout(1000)
        home_page.wait_for_selector("#books-table-container table", timeout=5000)

        toast = home_page.locator("#toast")
        expect(toast).to_contain_text("deleted successfully")

        new_count = home_page.locator("#books-table-container table tbody tr").count()
        assert new_count == initial_count - 1


class TestModalBehavior:
    """Tests for modal open/close behavior."""

    def test_close_modal_with_x_button(self, home_page):
        home_page.locator("#add-book-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        home_page.locator(".modal-close").click()
        expect(modal).to_have_class(re.compile(r"hidden"))

    def test_close_modal_with_overlay_click(self, home_page):
        home_page.locator("#add-book-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        home_page.locator(".modal-overlay").click(force=True)
        expect(modal).to_have_class(re.compile(r"hidden"))

    def test_close_modal_with_escape(self, home_page):
        home_page.locator("#add-book-btn").click()

        modal = home_page.locator("#modal")
        expect(modal).not_to_have_class(re.compile(r"hidden"))

        home_page.keyboard.press("Escape")
        expect(modal).to_have_class(re.compile(r"hidden"))
