/**
 * ui.js
 * -----
 * UI setup, interactions and cursors logic.
 */

document.addEventListener('DOMContentLoaded', () => {
    // Dynamic Cursor SVG Data-URI Injection
    const cursorSvg = `data:image/svg+xml;utf8,<svg width="32" height="32" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><g transform="rotate(6, 12, 12)"><path d="M1.50001 4.07491C0.897091 2.46714 2.46715 0.897094 4.07491 1.50001L21.2155 7.92774C23.1217 8.64256 22.8657 11.4162 20.8609 11.77L13.1336 13.1336L11.77 20.8609C11.4162 22.8657 8.64255 23.1217 7.92774 21.2155L1.50001 4.07491Z" fill="%23000000"/><path d="M3.37267 3.37267L9.8004 20.5133L11.164 12.786C11.3101 11.9582 11.9582 11.3101 12.786 11.164L20.5133 9.8004L3.37267 3.37267Z" fill="%23FFFFFF"/></g></svg>`;
    const cursorPointerSvg = `data:image/svg+xml;utf8,<svg width="32" height="32" viewBox="0 0 36 36" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M30.74,15.19a13.66,13.66,0,0,0-6.87-3.83A26,26,0,0,0,18,10.58V5.28A3.4,3.4,0,0,0,14.5,2,3.4,3.4,0,0,0,11,5.28v10L9.4,13.7a3.77,3.77,0,0,0-5.28,0A3.67,3.67,0,0,0,3,16.33a3.6,3.6,0,0,0,1,2.56l4.66,5.52a11.53,11.53,0,0,0,1.43,4,10.12,10.12,0,0,0,2,2.54v1.92a1.07,1.07,0,0,0,1,1.08H27a1.07,1.07,0,0,0,1-1.08v-2.7a12.81,12.81,0,0,0,3-8.36v-6A1,1,0,0,0,30.74,15.19Z" fill="%23000000"/><path d="M29,21.86a10.72,10.72,0,0,1-2.6,7.26,1.11,1.11,0,0,0-.4.72V32H14.14V30.52a1,1,0,0,0-.44-.83,7.26,7.26,0,0,1-1.82-2.23,9.14,9.14,0,0,1-1.2-3.52,1,1,0,0,0-.23-.59L5.53,17.53a1.7,1.7,0,0,1,0-2.42,1.76,1.76,0,0,1,2.47,0l3,3v3.14l2-1V5.28A1.42,1.42,0,0,1,14.5,4,1.42,1.42,0,0,1,16,5.28v11.8l2,.43V12.59a24.27,24.27,0,0,1,2.51.18V18l1.6.35V13c.41.08.83.17,1.26.28a14.88,14.88,0,0,1,1.53.49v5.15l1.6.35V14.5A11.06,11.06,0,0,1,29,16.23Z" fill="%23FFFFFF"/></svg>`;

    document.documentElement.style.setProperty('--cursor-default', `url('${cursorSvg}') 2 2, auto`);
    document.documentElement.style.setProperty('--cursor-pointer', `url('${cursorPointerSvg}') 14 2, pointer`);

    // ---------------------------------------------------------
    // Experience Catalog View Mode Switcher (Standard vs Compact)
    // ---------------------------------------------------------
    const expGrid = document.getElementById('experiences-grid');
    const stdBtn = document.getElementById('view-standard-btn');
    const cmpBtn = document.getElementById('view-compact-btn');

    if (expGrid && stdBtn && cmpBtn) {
        const setViewMode = (mode) => {
            if (mode === 'compact') {
                expGrid.classList.add('view-compact');
                cmpBtn.classList.add('active');
                cmpBtn.setAttribute('aria-pressed', 'true');
                stdBtn.classList.remove('active');
                stdBtn.setAttribute('aria-pressed', 'false');
                try { localStorage.setItem('experiences_view_mode', 'compact'); } catch (e) {}
            } else {
                expGrid.classList.remove('view-compact');
                stdBtn.classList.add('active');
                stdBtn.setAttribute('aria-pressed', 'true');
                cmpBtn.classList.remove('active');
                cmpBtn.setAttribute('aria-pressed', 'false');
                try { localStorage.setItem('experiences_view_mode', 'standard'); } catch (e) {}
            }
        };

        // Load persisted user preference (default: standard)
        let savedMode = 'standard';
        try {
            savedMode = localStorage.getItem('experiences_view_mode') || 'standard';
        } catch (e) {}
        setViewMode(savedMode);

        stdBtn.addEventListener('click', () => setViewMode('standard'));
        cmpBtn.addEventListener('click', () => setViewMode('compact'));
    }
});
