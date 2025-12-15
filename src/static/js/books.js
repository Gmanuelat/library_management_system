/**
 * Books UI Component
 * Handles all book-related UI operations
 */

let booksData = [];
let authorsData = [];
let searchTimeout = null;

/**
 * Load and display all books
 */
async function loadBooks() {
    const container = document.getElementById('books-table-container');
    const loading = document.getElementById('books-loading');
    const error = document.getElementById('books-error');

    try {
        loading.classList.remove('hidden');
        error.classList.add('hidden');

        const response = await BooksAPI.getAll();
        booksData = response.data;

        renderBooksTable(booksData);
    } catch (err) {
        error.textContent = `Error loading books: ${err.message}`;
        error.classList.remove('hidden');
        container.innerHTML = '';
    } finally {
        loading.classList.add('hidden');
    }
}

/**
 * Load authors for dropdown
 */
async function loadAuthorsForDropdown() {
    try {
        const response = await AuthorsAPI.getAll();
        authorsData = response.data;
    } catch (err) {
        console.error('Error loading authors:', err);
        authorsData = [];
    }
}

/**
 * Render books table
 */
function renderBooksTable(books) {
    const container = document.getElementById('books-table-container');

    if (books.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No books found</h3>
                <p>Add your first book to get started!</p>
            </div>
        `;
        return;
    }

    const tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Title</th>
                    <th>Author</th>
                    <th>ISBN</th>
                    <th>Year</th>
                    <th>Genre</th>
                    <th>Copies</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${books.map(book => `
                    <tr>
                        <td>${book.id}</td>
                        <td>${escapeHtml(book.title)}</td>
                        <td>${book.author_name ? escapeHtml(book.author_name) : 'N/A'}</td>
                        <td>${escapeHtml(book.isbn)}</td>
                        <td>${book.year || 'N/A'}</td>
                        <td>${book.genre ? escapeHtml(book.genre) : 'N/A'}</td>
                        <td>${book.copies}</td>
                        <td class="actions-cell">
                            <button class="btn btn-primary btn-small" onclick="editBook(${book.id})">Edit</button>
                            <button class="btn btn-danger btn-small" onclick="deleteBook(${book.id})">Delete</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    container.innerHTML = tableHTML;
}

/**
 * Show add book form
 */
async function showAddBookForm() {
    await loadAuthorsForDropdown();

    const authorOptions = authorsData.map(author =>
        `<option value="${author.id}">${escapeHtml(author.name)}</option>`
    ).join('');

    const formHTML = `
        <h2>Add New Book</h2>
        <form id="book-form" onsubmit="handleBookSubmit(event)">
            <div class="form-group">
                <label for="book-title">Title *</label>
                <input type="text" id="book-title" name="title" required>
            </div>
            <div class="form-group">
                <label for="book-isbn">ISBN *</label>
                <input type="text" id="book-isbn" name="isbn" required>
            </div>
            <div class="form-group">
                <label for="book-year">Publication Year</label>
                <input type="number" id="book-year" name="year" min="1000" max="2100">
            </div>
            <div class="form-group">
                <label for="book-genre">Genre</label>
                <input type="text" id="book-genre" name="genre">
            </div>
            <div class="form-group">
                <label for="book-copies">Number of Copies</label>
                <input type="number" id="book-copies" name="copies" value="1" min="1">
            </div>
            <div class="form-group">
                <label for="book-author">Author</label>
                <select id="book-author" name="author_id">
                    <option value="">-- No Author --</option>
                    ${authorOptions}
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-primary">Add Book</button>
            </div>
        </form>
    `;

    showModal(formHTML);
}

/**
 * Show edit book form
 */
async function editBook(bookId) {
    await loadAuthorsForDropdown();

    const book = booksData.find(b => b.id === bookId);
    if (!book) {
        showToast('Book not found', 'error');
        return;
    }

    const authorOptions = authorsData.map(author =>
        `<option value="${author.id}" ${book.author_id === author.id ? 'selected' : ''}>
            ${escapeHtml(author.name)}
        </option>`
    ).join('');

    const formHTML = `
        <h2>Edit Book</h2>
        <form id="book-form" onsubmit="handleBookSubmit(event, ${bookId})">
            <div class="form-group">
                <label for="book-title">Title *</label>
                <input type="text" id="book-title" name="title" value="${escapeHtml(book.title)}" required>
            </div>
            <div class="form-group">
                <label for="book-isbn">ISBN *</label>
                <input type="text" id="book-isbn" name="isbn" value="${escapeHtml(book.isbn)}" required>
            </div>
            <div class="form-group">
                <label for="book-year">Publication Year</label>
                <input type="number" id="book-year" name="year" value="${book.year || ''}" min="1000" max="2100">
            </div>
            <div class="form-group">
                <label for="book-genre">Genre</label>
                <input type="text" id="book-genre" name="genre" value="${book.genre || ''}">
            </div>
            <div class="form-group">
                <label for="book-copies">Number of Copies</label>
                <input type="number" id="book-copies" name="copies" value="${book.copies}" min="1">
            </div>
            <div class="form-group">
                <label for="book-author">Author</label>
                <select id="book-author" name="author_id">
                    <option value="">-- No Author --</option>
                    ${authorOptions}
                </select>
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-success">Update Book</button>
            </div>
        </form>
    `;

    showModal(formHTML);
}

/**
 * Handle book form submission
 */
async function handleBookSubmit(event, bookId = null) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const bookData = {
        title: formData.get('title'),
        isbn: formData.get('isbn'),
        year: formData.get('year') ? parseInt(formData.get('year')) : null,
        genre: formData.get('genre') || null,
        copies: formData.get('copies') ? parseInt(formData.get('copies')) : 1,
        author_id: formData.get('author_id') ? parseInt(formData.get('author_id')) : null
    };

    try {
        if (bookId) {
            // Update existing book
            await BooksAPI.update(bookId, bookData);
            showToast('Book updated successfully', 'success');
        } else {
            // Create new book
            await BooksAPI.create(bookData);
            showToast('Book added successfully', 'success');
        }

        closeModal();
        await loadBooks();
    } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
    }
}

/**
 * Delete book with confirmation
 */
async function deleteBook(bookId) {
    const book = booksData.find(b => b.id === bookId);
    if (!book) {
        showToast('Book not found', 'error');
        return;
    }

    if (!confirm(`Are you sure you want to delete "${book.title}"?`)) {
        return;
    }

    try {
        await BooksAPI.delete(bookId);
        showToast('Book deleted successfully', 'success');
        await loadBooks();
    } catch (err) {
        showToast(`Error deleting book: ${err.message}`, 'error');
    }
}

/**
 * Handle book search
 */
async function handleBookSearch(query) {
    const container = document.getElementById('books-table-container');
    const loading = document.getElementById('books-loading');
    const error = document.getElementById('books-error');

    // Clear previous timeout
    if (searchTimeout) {
        clearTimeout(searchTimeout);
    }

    // If query is empty, load all books
    if (!query.trim()) {
        await loadBooks();
        return;
    }

    // Debounce search
    searchTimeout = setTimeout(async () => {
        try {
            loading.classList.remove('hidden');
            error.classList.add('hidden');

            const response = await BooksAPI.search(query);
            booksData = response.data;

            renderBooksTable(booksData);
        } catch (err) {
            error.textContent = `Error searching books: ${err.message}`;
            error.classList.remove('hidden');
            container.innerHTML = '';
        } finally {
            loading.classList.add('hidden');
        }
    }, 300);
}

/**
 * Initialize books section
 */
function initBooks() {
    // Add button click handler
    document.getElementById('add-book-btn').addEventListener('click', showAddBookForm);

    // Search input handler
    document.getElementById('books-search').addEventListener('input', (e) => {
        handleBookSearch(e.target.value);
    });

    // Load books initially
    loadBooks();
}
