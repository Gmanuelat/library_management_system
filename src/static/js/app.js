/**
 * Main Application Controller
 * Handles initialization, navigation, modals, and global utilities
 */

// Current active section
let currentSection = 'books';

/**
 * Initialize the application
 */
document.addEventListener('DOMContentLoaded', () => {
    console.log('Library Management System initialized');

    // Initialize navigation
    initNavigation();

    // Initialize modal
    initModal();

    // Initialize books and authors sections
    initBooks();
    initAuthors();

    // Show books section by default
    showSection('books');
});

/**
 * Initialize navigation
 */
function initNavigation() {
    const booksNavBtn = document.getElementById('nav-books');
    const authorsNavBtn = document.getElementById('nav-authors');

    booksNavBtn.addEventListener('click', () => {
        showSection('books');
    });

    authorsNavBtn.addEventListener('click', () => {
        showSection('authors');
    });
}

/**
 * Show specific section and update navigation
 */
function showSection(sectionName) {
    // Hide all sections
    const sections = document.querySelectorAll('.section');
    sections.forEach(section => section.classList.remove('active'));

    // Remove active class from all nav buttons
    const navButtons = document.querySelectorAll('.nav-btn');
    navButtons.forEach(btn => btn.classList.remove('active'));

    // Show selected section
    const targetSection = document.getElementById(`${sectionName}-section`);
    const targetNavBtn = document.getElementById(`nav-${sectionName}`);

    if (targetSection && targetNavBtn) {
        targetSection.classList.add('active');
        targetNavBtn.classList.add('active');
        currentSection = sectionName;
    }
}

/**
 * Initialize modal functionality
 */
function initModal() {
    const modal = document.getElementById('modal');
    const modalClose = document.querySelector('.modal-close');
    const modalOverlay = document.querySelector('.modal-overlay');

    // Close modal on X button click
    modalClose.addEventListener('click', closeModal);

    // Close modal on overlay click
    modalOverlay.addEventListener('click', closeModal);

    // Close modal on ESC key
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && !modal.classList.contains('hidden')) {
            closeModal();
        }
    });
}

/**
 * Show modal with content
 */
function showModal(content) {
    const modal = document.getElementById('modal');
    const modalBody = document.getElementById('modal-body');

    modalBody.innerHTML = content;
    modal.classList.remove('hidden');
}

/**
 * Close modal
 */
function closeModal() {
    const modal = document.getElementById('modal');
    modal.classList.add('hidden');
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');

    toast.textContent = message;
    toast.className = 'toast'; // Reset classes

    if (type === 'success') {
        toast.classList.add('success');
    } else if (type === 'error') {
        toast.classList.add('error');
    }

    toast.classList.remove('hidden');

    // Auto-hide after 3 seconds
    setTimeout(() => {
        toast.classList.add('hidden');
    }, 3000);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    if (text === null || text === undefined) {
        return '';
    }

    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Format date to readable string
 */
function formatDate(dateString) {
    if (!dateString) return 'N/A';

    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
}

/**
 * Global error handler
 */
window.addEventListener('error', (event) => {
    console.error('Global error:', event.error);
});

/**
 * Global unhandled promise rejection handler
 */
window.addEventListener('unhandledrejection', (event) => {
    console.error('Unhandled promise rejection:', event.reason);
});
