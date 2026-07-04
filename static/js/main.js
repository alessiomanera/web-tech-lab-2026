document.addEventListener('DOMContentLoaded', () => {
    // Booking Form Polite Error Handling
    const bookingForm = document.getElementById('booking-form');
    
    if (bookingForm) {
        bookingForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            const museumSelect = document.getElementById('museum-select');
            const dateInput = document.getElementById('visit-date');
            
            let isValid = true;
            
            // Reset previous errors
            document.getElementById('museum-group').classList.remove('has-error');
            document.getElementById('date-group').classList.remove('has-error');
            
            // Validate Museum
            if (!museumSelect.value) {
                document.getElementById('museum-group').classList.add('has-error');
                isValid = false;
            }
            
            // Validate Date (must be selected and in the future/today)
            if (!dateInput.value) {
                document.getElementById('date-group').classList.add('has-error');
                isValid = false;
            } else {
                const selectedDate = new Date(dateInput.value);
                const today = new Date();
                today.setHours(0, 0, 0, 0); // Reset time for accurate day comparison
                
                if (selectedDate < today) {
                    const errorSpan = document.getElementById('date-error');
                    errorSpan.textContent = "Please select a date that is today or in the future.";
                    document.getElementById('date-group').classList.add('has-error');
                    isValid = false;
                }
            }
            
            if (isValid) {
                // In Phase 5, this will be an async fetch call to the backend.
                // For now, we simulate a successful polite booking.
                const btn = bookingForm.querySelector('button[type="submit"]');
                const originalText = btn.textContent;
                
                btn.textContent = "Booking Confirmed! 🎉";
                btn.style.background = "var(--success-color)";
                
                setTimeout(() => {
                    // Reset styling for demo purposes
                    btn.textContent = originalText;
                    btn.style.background = "";
                    bookingForm.reset();
                }, 2000);
            }
        });
        
        // Remove error state politely when user starts typing/selecting
        const inputs = bookingForm.querySelectorAll('input, select');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                input.closest('.form-group').classList.remove('has-error');
            });
        });
    }
});
