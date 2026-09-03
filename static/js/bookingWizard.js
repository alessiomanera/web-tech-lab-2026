/**
 * bookingWizard.js
 * ----------------
 * 4-Step Frictionless Booking Wizard Controller
 * Manages state transitions, dynamic addon price calculations, time-slot selection,
 * and asynchronous booking submission.
 */

document.addEventListener('DOMContentLoaded', () => {
    // -------------------------------------------------------------------------
    // State Management for the multi-step booking wizard
    // -------------------------------------------------------------------------
    const state = {
        currentStep: 1,
        experienceId: null,
        experienceTitle: '',
        city: '',
        duration: 0,
        basePrice: 0.0,
        availableAddons: [],
        selectedAddons: [],
        visitDate: '',
        timeSlot: '', // set below from whichever pill the server rendered as active
        guestsCount: 1,
        totalPrice: 0.0
    };

    // DOM Elements
    const expSelect = document.getElementById('exp-select');
    const previewBox = document.getElementById('experience-preview-box');
    const previewTitle = document.getElementById('preview-title');
    const previewCity = document.getElementById('preview-city');
    const previewDesc = document.getElementById('preview-desc');
    const addonsContainer = document.getElementById('addons-container');
    const step1Price = document.getElementById('step1-price');
    const dateInput = document.getElementById('visit-date');
    const guestsSelect = document.getElementById('guests-count');
    const timeSlots = document.querySelectorAll('.time-slot-pill');
    const errorMsg = document.getElementById('booking-error-msg');

    // The list of valid slots lives server-side (routes.py VALID_TIME_SLOTS);
    // read the one the template marked active instead of hardcoding a copy here.
    const initialActiveSlot = document.querySelector('.time-slot-pill.active') || timeSlots[0];
    if (initialActiveSlot) {
        state.timeSlot = initialActiveSlot.getAttribute('data-slot');
    }

    // Setup Date Picker Bounds (Today to +90 Days)
    if (dateInput) {
        const today = new Date();
        const yyyy = today.getFullYear();
        const mm = String(today.getMonth() + 1).padStart(2, '0');
        const dd = String(today.getDate()).padStart(2, '0');
        dateInput.min = `${yyyy}-${mm}-${dd}`;
        dateInput.value = `${yyyy}-${mm}-${dd}`;
        state.visitDate = `${yyyy}-${mm}-${dd}`;

        const maxDate = new Date(today.getTime() + 90 * 24 * 60 * 60 * 1000);
        const max_yyyy = maxDate.getFullYear();
        const max_mm = String(maxDate.getMonth() + 1).padStart(2, '0');
        const max_dd = String(maxDate.getDate()).padStart(2, '0');
        dateInput.max = `${max_yyyy}-${max_mm}-${max_dd}`;
    }

    // -------------------------------------------------------------------------
    // Step Navigation Handlers
    // -------------------------------------------------------------------------
    function showStep(step) {
        state.currentStep = step;
        
        // Update Panel Visibility
        for (let i = 1; i <= 4; i++) {
            const panel = document.getElementById(`panel-${i}`);
            const node = document.getElementById(`node-${i}`);
            if (panel) panel.classList.toggle('active', i === step);
            if (node) {
                node.classList.toggle('active', i === step);
                node.classList.toggle('completed', i < step);
            }
        }
    }

    // Dynamic Price Calculation
    function calculateTotal() {
        const guests = parseInt(state.guestsCount, 10) || 1;
        const baseTotal = state.basePrice * guests;
        const addonsTotal = state.selectedAddons.reduce((sum, item) => sum + item.price, 0) * guests;
        state.totalPrice = baseTotal + addonsTotal;

        if (step1Price) {
            step1Price.textContent = `€${state.totalPrice.toFixed(2)}`;
        }
    }

    // Render Addons for Selected Experience
    function renderAddons(addons) {
        state.availableAddons = addons;
        state.selectedAddons = [];
        addonsContainer.innerHTML = '';

        if (!addons || addons.length === 0) {
            addonsContainer.innerHTML = '<p class="addon-empty-note">No optional add-ons available for this package.</p>';
            calculateTotal();
            return;
        }

        addons.forEach((addon, idx) => {
            const card = document.createElement('div');
            card.className = 'addon-choice-card';
            card.setAttribute('data-id', addon.id);
            card.innerHTML = `
                <div class="addon-choice-row">
                    <input type="checkbox" id="addon-${idx}" class="addon-checkbox">
                    <label for="addon-${idx}" class="addon-label"></label>
                </div>
                <span class="addon-price">+€${parseFloat(addon.price).toFixed(2)}</span>
            `;
            // Set as text, never interpolated into the markup above: an add-on
            // name is data, and data must never be able to become markup.
            card.querySelector('.addon-label').textContent = addon.name;

            const checkbox = card.querySelector('input[type="checkbox"]');
            
            card.addEventListener('click', (e) => {
                // A click on the <label> is already forwarded to the checkbox by
                // the browser, which fires a second click on the checkbox itself.
                // Toggling here as well would undo it, so let that one do the work.
                if (e.target.closest('label')) return;

                if (e.target !== checkbox) {
                    checkbox.checked = !checkbox.checked;
                }
                card.classList.toggle('selected', checkbox.checked);

                if (checkbox.checked) {
                    state.selectedAddons.push(addon);
                } else {
                    state.selectedAddons = state.selectedAddons.filter(a => a.id !== addon.id);
                }
                calculateTotal();
            });

            addonsContainer.appendChild(card);
        });

        calculateTotal();
    }

    // Handle Experience Selection Change
    function handleExperienceChange() {
        const selectedOption = expSelect.options[expSelect.selectedIndex];
        if (!selectedOption || !selectedOption.value) return;

        state.experienceId = selectedOption.value;
        state.basePrice = parseFloat(selectedOption.getAttribute('data-price')) || 0;
        state.city = selectedOption.getAttribute('data-city') || '';
        state.duration = selectedOption.getAttribute('data-duration') || '';
        
        let addons = [];
        try {
            addons = JSON.parse(selectedOption.getAttribute('data-addons') || '[]');
        } catch (e) {
            addons = [];
        }

        // Update preview
        previewBox.classList.remove('is-hidden');
        previewTitle.textContent = selectedOption.text.split('|')[0].trim();
        state.experienceTitle = previewTitle.textContent;
        previewCity.textContent = state.city;
        previewDesc.textContent = `Curated ${state.duration}-minute journey with priority access.`;

        renderAddons(addons);
    }

    if (expSelect) {
        expSelect.addEventListener('change', handleExperienceChange);
        // If pre-selected on page load
        if (expSelect.value) {
            handleExperienceChange();
        }
    }

    // Time Slot Selection
    timeSlots.forEach(pill => {
        pill.addEventListener('click', () => {
            timeSlots.forEach(p => {
                p.classList.remove('active');
                p.setAttribute('aria-pressed', 'false');
            });
            pill.classList.add('active');
            pill.setAttribute('aria-pressed', 'true');
            state.timeSlot = pill.getAttribute('data-slot');
        });
    });

    if (dateInput) {
        dateInput.addEventListener('change', () => {
            state.visitDate = dateInput.value;
        });
    }

    if (guestsSelect) {
        guestsSelect.addEventListener('change', () => {
            state.guestsCount = parseInt(guestsSelect.value, 10);
            calculateTotal();
        });
    }

    // -------------------------------------------------------------------------
    // Step Button Transitions
    // -------------------------------------------------------------------------
    const btnToStep2 = document.getElementById('btn-to-step2');
    const btnBackToStep1 = document.getElementById('btn-back-to-step1');
    const btnToStep3 = document.getElementById('btn-to-step3');
    const btnBackToStep2 = document.getElementById('btn-back-to-step2');
    const btnConfirm = document.getElementById('btn-confirm-booking');

    if (btnToStep2) {
        btnToStep2.addEventListener('click', () => {
            if (!state.experienceId) {
                alert('Please select a cultural experience package first.');
                return;
            }
            showStep(2);
        });
    }

    if (btnBackToStep1) {
        btnBackToStep1.addEventListener('click', () => showStep(1));
    }

    if (btnToStep3) {
        btnToStep3.addEventListener('click', () => {
            if (!dateInput.value) {
                alert('Please pick a visit date.');
                return;
            }
            state.visitDate = dateInput.value;
            calculateTotal();

            // Populate Step 3 Summary
            document.getElementById('summary-exp-title').textContent = state.experienceTitle;
            document.getElementById('summary-exp-city').textContent = state.city;
            document.getElementById('summary-date').textContent = state.visitDate;
            document.getElementById('summary-slot').textContent = state.timeSlot;
            document.getElementById('summary-guests').textContent = `${state.guestsCount} Guest(s)`;
            
            const addonNames = state.selectedAddons.map(a => a.name).join(', ');
            document.getElementById('summary-addons').textContent = addonNames || 'None (Standard Package)';
            document.getElementById('summary-total-price').textContent = `€${state.totalPrice.toFixed(2)}`;

            showStep(3);
        });
    }

    if (btnBackToStep2) {
        btnBackToStep2.addEventListener('click', () => showStep(2));
    }

    // -------------------------------------------------------------------------
    // Step 4: Submission to API
    // -------------------------------------------------------------------------
    if (btnConfirm) {
        btnConfirm.addEventListener('click', () => {
            if (errorMsg) errorMsg.style.display = 'none';
            
            // Client-side validation as a UX nicety
            if (!state.experienceId) {
                alert('Please select a cultural experience package first.');
                return;
            }
            if (!state.visitDate) {
                alert('Please pick a visit date.');
                return;
            }

            btnConfirm.disabled = true;
            btnConfirm.textContent = 'Securing Your Pass...';

            // Populate the form hidden fields
            const hiddenExpId = document.getElementById('hidden-experience-id');
            const hiddenDate = document.getElementById('hidden-visit-date');
            const hiddenSlot = document.getElementById('hidden-time-slot');
            const hiddenGuests = document.getElementById('hidden-guests-count');
            const hiddenAddons = document.getElementById('hidden-selected-addons-json');
            const form = document.getElementById('booking-form');

            if (hiddenExpId) hiddenExpId.value = state.experienceId;
            if (hiddenDate) hiddenDate.value = state.visitDate;
            if (hiddenSlot) hiddenSlot.value = state.timeSlot;
            if (hiddenGuests) hiddenGuests.value = state.guestsCount;
            if (hiddenAddons) hiddenAddons.value = JSON.stringify(state.selectedAddons);

            if (form) {
                form.submit();
            }
        });
    }
});
