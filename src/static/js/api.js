/**
 * API Client for Library Management System
 * Handles all HTTP requests to the Flask backend
 */

const API_BASE_URL = 'http://localhost:5001/api';

/**
 * Generic fetch wrapper with error handling
 */
async function apiRequest(url, options = {}) {
    try {
        const response = await fetch(url, {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            ...options
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.error || `HTTP error! status: ${response.status}`);
        }

        return data;
    } catch (error) {
        console.error('API request failed:', error);
        throw error;
    }
}

/**
 * Book API methods
 */
const BooksAPI = {
    /**
     * Get all books
     */
    async getAll() {
        return apiRequest(`${API_BASE_URL}/books`);
    },

    /**
     * Get book by ID
     */
    async getById(id) {
        return apiRequest(`${API_BASE_URL}/books/${id}`);
    },

    /**
     * Create new book
     */
    async create(bookData) {
        return apiRequest(`${API_BASE_URL}/books`, {
            method: 'POST',
            body: JSON.stringify(bookData)
        });
    },

    /**
     * Update book
     */
    async update(id, bookData) {
        return apiRequest(`${API_BASE_URL}/books/${id}`, {
            method: 'PUT',
            body: JSON.stringify(bookData)
        });
    },

    /**
     * Delete book
     */
    async delete(id) {
        return apiRequest(`${API_BASE_URL}/books/${id}`, {
            method: 'DELETE'
        });
    },

    /**
     * Search books
     */
    async search(query) {
        return apiRequest(`${API_BASE_URL}/books/search?q=${encodeURIComponent(query)}`);
    },

    /**
     * Get book count
     */
    async getCount() {
        return apiRequest(`${API_BASE_URL}/books/count`);
    }
};

/**
 * Author API methods
 */
const AuthorsAPI = {
    /**
     * Get all authors
     */
    async getAll() {
        return apiRequest(`${API_BASE_URL}/authors`);
    },

    /**
     * Get author by ID
     */
    async getById(id) {
        return apiRequest(`${API_BASE_URL}/authors/${id}`);
    },

    /**
     * Create new author
     */
    async create(authorData) {
        return apiRequest(`${API_BASE_URL}/authors`, {
            method: 'POST',
            body: JSON.stringify(authorData)
        });
    },

    /**
     * Update author
     */
    async update(id, authorData) {
        return apiRequest(`${API_BASE_URL}/authors/${id}`, {
            method: 'PUT',
            body: JSON.stringify(authorData)
        });
    },

    /**
     * Delete author
     */
    async delete(id) {
        return apiRequest(`${API_BASE_URL}/authors/${id}`, {
            method: 'DELETE'
        });
    },

    /**
     * Search authors
     */
    async search(query) {
        return apiRequest(`${API_BASE_URL}/authors/search?q=${encodeURIComponent(query)}`);
    },

    /**
     * Get author count
     */
    async getCount() {
        return apiRequest(`${API_BASE_URL}/authors/count`);
    }
};
