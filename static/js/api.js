/**
 * api.js
 * ------
 * API service helper functions for async fetch operations.
 */

/**
 * Reads the per-session CSRF token that base.html embeds in a meta tag.
 * The server rejects any state-changing request that does not echo it back.
 */
function csrfToken() {
    const tag = document.querySelector('meta[name="csrf-token"]');
    return tag ? tag.getAttribute('content') : '';
}

/** Standard headers for a JSON POST, including the CSRF token. */
function jsonHeaders() {
    return { 'Content-Type': 'application/json', 'X-CSRFToken': csrfToken() };
}

const ApiService = {
    async submitFeedback(bookingId, rating, comment) {
        const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: jsonHeaders(),
            body: JSON.stringify({ booking_id: bookingId, rating, comment })
        });
        return res;
    },

    async resetMemory() {
        const res = await fetch('/api/profile/reset-memory', {
            method: 'POST',
            headers: { 'X-CSRFToken': csrfToken() }
        });
        return res;
    },

    async sendChatMessage(message) {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: jsonHeaders(),
            body: JSON.stringify({ message })
        });
        return res;
    }
};
