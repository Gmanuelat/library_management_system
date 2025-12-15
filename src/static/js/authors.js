/**
 * Authors UI Component
 * Handles all author-related UI operations
 */

let authorsListData = [];
let authorSearchTimeout = null;

/**
 * Load and display all authors
 */
async function loadAuthors() {
    const container = document.getElementById('authors-table-container');
    const loading = document.getElementById('authors-loading');
    const error = document.getElementById('authors-error');

    try {
        loading.classList.remove('hidden');
        error.classList.add('hidden');

        const response = await AuthorsAPI.getAll();
        authorsListData = response.data;

        renderAuthorsTable(authorsListData);
    } catch (err) {
        error.textContent = `Error loading authors: ${err.message}`;
        error.classList.remove('hidden');
        container.innerHTML = '';
    } finally {
        loading.classList.add('hidden');
    }
}

/**
 * Render authors table
 */
function renderAuthorsTable(authors) {
    const container = document.getElementById('authors-table-container');

    if (authors.length === 0) {
        container.innerHTML = `
            <div class="empty-state">
                <h3>No authors found</h3>
                <p>Add your first author to get started!</p>
            </div>
        `;
        return;
    }

    const tableHTML = `
        <table>
            <thead>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Birth Year</th>
                    <th>Nationality</th>
                    <th>Actions</th>
                </tr>
            </thead>
            <tbody>
                ${authors.map(author => `
                    <tr>
                        <td>${author.id}</td>
                        <td>${escapeHtml(author.name)}</td>
                        <td>${author.birth_year || 'N/A'}</td>
                        <td>${author.nationality ? escapeHtml(author.nationality) : 'N/A'}</td>
                        <td class="actions-cell">
                            <button class="btn btn-primary btn-small" onclick="editAuthor(${author.id})">Edit</button>
                            <button class="btn btn-danger btn-small" onclick="deleteAuthor(${author.id})">Delete</button>
                        </td>
                    </tr>
                `).join('')}
            </tbody>
        </table>
    `;

    container.innerHTML = tableHTML;
}

/**
 * Show add author form
 */
function showAddAuthorForm() {
    const formHTML = `
        <h2>Add New Author</h2>
        <form id="author-form" onsubmit="handleAuthorSubmit(event)">
            <div class="form-group">
                <label for="author-name">Name *</label>
                <input type="text" id="author-name" name="name" required>
            </div>
            <div class="form-group">
                <label for="author-birth-year">Birth Year</label>
                <input type="number" id="author-birth-year" name="birth_year" min="1000" max="2100">
            </div>
            <div class="form-group">
                <label for="author-nationality">Nationality</label>
                <input type="text" id="author-nationality" name="nationality">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-success">Add Author</button>
            </div>
        </form>
    `;

    showModal(formHTML);
}

/**
 * Show edit author form
 */
function editAuthor(authorId) {
    const author = authorsListData.find(a => a.id === authorId);
    if (!author) {
        showToast('Author not found', 'error');
        return;
    }

    const formHTML = `
        <h2>Edit Author</h2>
        <form id="author-form" onsubmit="handleAuthorSubmit(event, ${authorId})">
            <div class="form-group">
                <label for="author-name">Name *</label>
                <input type="text" id="author-name" name="name" value="${escapeHtml(author.name)}" required>
            </div>
            <div class="form-group">
                <label for="author-birth-year">Birth Year</label>
                <input type="number" id="author-birth-year" name="birth_year" value="${author.birth_year || ''}" min="1000" max="2100">
            </div>
            <div class="form-group">
                <label for="author-nationality">Nationality</label>
                <input type="text" id="author-nationality" name="nationality" value="${author.nationality || ''}">
            </div>
            <div class="form-actions">
                <button type="button" class="btn btn-secondary" onclick="closeModal()">Cancel</button>
                <button type="submit" class="btn btn-success">Update Author</button>
            </div>
        </form>
    `;

    showModal(formHTML);
}

/**
 * Handle author form submission
 */
async function handleAuthorSubmit(event, authorId = null) {
    event.preventDefault();

    const form = event.target;
    const formData = new FormData(form);

    const authorData = {
        name: formData.get('name'),
        birth_year: formData.get('birth_year') ? parseInt(formData.get('birth_year')) : null,
        nationality: formData.get('nationality') || null
    };

    try {
        if (authorId) {
            // Update existing author
            await AuthorsAPI.update(authorId, authorData);
            showToast('Author updated successfully', 'success');
        } else {
            // Create new author
            await AuthorsAPI.create(authorData);
            showToast('Author added successfully', 'success');
        }

        closeModal();
        await loadAuthors();
    } catch (err) {
        showToast(`Error: ${err.message}`, 'error');
    }
}

/**
 * Delete author with confirmation
 */
async function deleteAuthor(authorId) {
    const author = authorsListData.find(a => a.id === authorId);
    if (!author) {
        showToast('Author not found', 'error');
        return;
    }

    if (!confirm(`Are you sure you want to delete "${author.name}"?\n\nNote: This will fail if the author has books linked to them.`)) {
        return;
    }

    try {
        await AuthorsAPI.delete(authorId);
        showToast('Author deleted successfully', 'success');
        await loadAuthors();
    } catch (err) {
        showToast(`Error deleting author: ${err.message}`, 'error');
    }
}

/**
 * Handle author search
 */
async function handleAuthorSearch(query) {
    const container = document.getElementById('authors-table-container');
    const loading = document.getElementById('authors-loading');
    const error = document.getElementById('authors-error');

    // Clear previous timeout
    if (authorSearchTimeout) {
        clearTimeout(authorSearchTimeout);
    }

    // If query is empty, load all authors
    if (!query.trim()) {
        await loadAuthors();
        return;
    }

    // Debounce search
    authorSearchTimeout = setTimeout(async () => {
        try {
            loading.classList.remove('hidden');
            error.classList.add('hidden');

            const response = await AuthorsAPI.search(query);
            authorsListData = response.data;

            renderAuthorsTable(authorsListData);
        } catch (err) {
            error.textContent = `Error searching authors: ${err.message}`;
            error.classList.remove('hidden');
            container.innerHTML = '';
        } finally {
            loading.classList.add('hidden');
        }
    }, 300);
}

/**
 * Initialize authors section
 */
function initAuthors() {
    // Add button click handler
    document.getElementById('add-author-btn').addEventListener('click', showAddAuthorForm);

    // Search input handler
    document.getElementById('authors-search').addEventListener('input', (e) => {
        handleAuthorSearch(e.target.value);
    });

    // Load authors initially
    loadAuthors();
}
