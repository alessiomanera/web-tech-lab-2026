/**
 * profile.js
 * ----------
 * Account dashboard controller: post-visit feedback submission and
 * taste-memory reset. No-ops on pages without feedback forms.
 */
document.addEventListener('DOMContentLoaded', () => {
    document.querySelectorAll('.feedback-form').forEach(form => {
        form.addEventListener('submit', async (e) => {
            e.preventDefault();
            const bookingId = form.getAttribute('data-booking-id');
            const rating = form.querySelector('[name="rating"]').value;
            const comment = form.querySelector('[name="comment"]').value;
            const btn = form.querySelector('button[type="submit"]');

            btn.disabled = true;
            btn.textContent = 'Submitting...';

            try {
                const res = await ApiService.submitFeedback(bookingId, rating, comment);
                if (res.ok) {
                    window.location.reload();
                    return;
                }
                const data = await res.json().catch(() => ({}));
                alert(data.error || 'Could not submit feedback.');
            } catch (err) {
                alert('Network error. Please try again.');
            }
            btn.disabled = false;
            btn.textContent = 'Submit Feedback';
        });
    });

    const resetBtn = document.getElementById('profile-reset-btn');
    if (resetBtn) {
        resetBtn.addEventListener('click', async () => {
            if (!confirm('Are you sure you want to clear your AI Taste Profile?')) return;
            try {
                const res = await ApiService.resetMemory();
                if (res.ok) window.location.reload();
            } catch (err) {
                alert('Network error. Please try again.');
            }
        });
    }
});
