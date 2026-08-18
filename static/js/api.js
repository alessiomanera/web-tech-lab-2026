/**
 * api.js
 * ------
 * API service helper functions for async fetch operations.
 */

const ApiService = {
    async submitFeedback(bookingId, rating, comment) {
        const res = await fetch('/api/feedback', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ booking_id: bookingId, rating, comment })
        });
        return res;
    },

    async resetMemory() {
        const res = await fetch('/api/profile/reset-memory', { method: 'POST' });
        return res;
    },

    async sendChatMessage(message) {
        const res = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });
        return res;
    }
};
