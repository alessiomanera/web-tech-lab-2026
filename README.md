# Museum Ticketing & AI Cultural Guide

**Author:** Alessio Manera  
**Student ID:** 905639  
**Course:** Lab of Web Technologies (AY 2025–26)  
**Group:** Group-11 (Single-person group)

---

## Project Overview

A full-stack web application designed for discovering and booking tickets to museums and cultural heritage sites in Italy, integrated with an AI-powered cultural concierge. The platform combines a streamlined e-ticketing workflow with an intelligent conversational assistant powered by Google Gemini, offering personalized visit recommendations grounded directly in the site's SQLite relational database.

---

## Technical Stack & Architecture

- **Frontend:** HTML5 (semantic markup, Jinja2 template inheritance), Vanilla CSS3 (custom Neubrutalist design system loaded directly without build tools), Vanilla JavaScript (ES6+ for asynchronous `fetch` requests and dynamic UI state machines).
- **Backend:** Python 3 with the Flask framework (modular Blueprint architecture: `routes.py`, `auth.py`).
- **Database & Storage:** Raw SQLite3 using parameterized queries (Python standard library `sqlite3`), no ORM helper libraries (`database.py`, `schema.sql`).
- **AI Engine (Module 4, core feature):** Google Gemini API (`gemini-2.5-flash`, configurable via `GEMINI_MODEL`) via the official `google-generativeai` SDK, implementing Retrieval-Augmented Generation (RAG) over the `experiences` SQLite catalog with persistent taste-profile extraction. Requires `GEMINI_API_KEY`. A deterministic keyword-matching fallback (no RAG, no profile updates) keeps the app usable without a key or during an API outage — a labelled safety net, not an equivalent path.

---

## Design System & UI/UX (Neubrutalism)

The user interface strictly adheres to the **Neubrutalism** design philosophy (inspired by [neubrutalism.com](https://neubrutalism.com/)), engineered for extreme visual clarity, simplicity, and zero cognitive friction:

- **High-Contrast Canvas:** Stark white background (`#FFFFFF`) with solid black text and high-contrast `3px` solid black borders (`#000000`).
- **Hard Offset Drop-Shadows:** `4px 4px 0px 0px #000000` with zero blur for distinct depth separation.
- **Zero Border-Radius:** `0px` border-radius across all buttons, cards, modal dialogs, and input fields.
- **Vibrant Primary & Accent Colors** (canonical values from `static/css/variables.css`):
  - Coral Red: `#FF6B6B`
  - Sky Blue: `#74B9FF`
  - Bold Yellow: `#FFD23F` (micro-accents only, always on black text)
  - Soft Green: `#88D498`
- **Typography:** Strictly `Inter` (sans-serif) across all elements, with heavy font weights (800/900) for section headings and balanced typographic text-wrapping.
- **Tactile Micro-interactions:** Mechanical button press effect (`transform: translate(4px, 4px)` with shadow collapse on click/active).
- **Theme:** Dual high-contrast Light and Dark mode, toggled from the header and persisted in `localStorage`. An inline bootstrap script in `<head>` applies the stored (or system-preferred) theme before first paint to eliminate flash-of-unstyled-content.
- **Accessibility:** Strict WCAG AA contrast compliance across all interactive elements (with AAA on body text) and zero Cumulative Layout Shift (CLS).

---

## Project Structure

```text
web-tech-lab-2026/
├── app.py                 # Application factory and entry point
├── database.py            # SQLite connection context manager & initialization
├── schema.sql             # SQL database definition (tables for users, museums, experiences, tickets)
├── routes.py              # Main Blueprint: page routes and API endpoints (/booking, /api/chat, /api/feedback)
├── auth.py                # Authentication Blueprint: registration, login, logout, @login_required
├── seed.py                # Database population script with Top 12 Curated Italian Cultural Experiences
├── requirements.txt       # Python package dependencies
├── .env.example           # Template for environment variables (GEMINI_API_KEY, FLASK_SECRET_KEY)
├── ROADMAP.md             # Phased development roadmap
├── LICENSE                # MIT licence
├── DOCS/
│   ├── 1-Page_Project_Proposal.md # 1-page A4 project proposal (Official Frozen Submission)
│   ├── PROJECT_REPORT.md  # Moodle submission document (goals, run instructions, roles)
│   └── Competitor_Analysis.md # Comprehensive European/Italian market research & UX audit
├── tests/                 # Automated test suite (Standard Library unittest)
│   ├── __init__.py        # Test package initializer
│   ├── test_base.py       # BaseTestCase with isolated in-memory/temp SQLite database
│   ├── test_database.py   # Database PRAGMA foreign_keys & cascade constraints
│   ├── test_auth.py       # User registration, password hashing & session management
│   ├── test_catalog.py    # Directory filtering by city, theme, and keyword search
│   ├── test_booking.py    # 4-step booking wizard, pricing arithmetic & ticket generation
│   ├── test_concierge.py  # Grounded Gemini RAG, actionable cards & taste memory
│   ├── test_feedback.py   # Post-visit review loops & ownership security
│   └── test_errors.py     # Custom HTTP error pages (400, 404, 500) & profile dashboard
├── static/
│   ├── css/
│   │   ├── variables.css  # CSS custom properties (colors, borders, shadows, spacing, cursors)
│   │   ├── layout.css     # Grid and Flexbox responsive layout containers & custom cursors
│   │   ├── components.css # Neubrutalist UI components (cards, buttons, forms, alerts, wizard)
│   │   └── utilities.css  # Utility classes
│   ├── js/
│   │   ├── main.js        # Global entry point
│   │   ├── api.js         # Shared fetch layer used by concierge.js and profile.js (chat, feedback, reset taste profile)
│   │   ├── ui.js          # Theme switcher, cursor injection, catalog view mode, tactile UI state
│   │   ├── concierge.js   # AI Concierge chat controller with client-side HTML escaping
│   │   ├── profile.js     # Dashboard feedback submission and taste-memory reset
│   │   └── bookingWizard.js # 4-step wizard state machine and dynamic addon price calculations
│   └── images/            # Static image assets & custom SVG cursors
└── templates/
    ├── base.html          # Master Jinja2 layout with navigation and alerts
    ├── index.html         # Landing page with 3-step value workflow & trending packages
    ├── experiences.html   # Full 12-Experience catalog with search & city filter pills
    ├── experience_detail.html # Deep-dive view for individual experiences
    ├── museums.html       # Cultural institutions directory
    ├── booking.html       # 4-step frictionless booking wizard
    ├── guide.html         # AI Cultural Concierge conversational chat view with taste memory
    ├── profile.html       # User dashboard: active digital passes, review loop, taste profile
    ├── login.html         # User login form
    ├── register.html      # User registration form with cultural preferences selector
    ├── 400.html           # Custom 400 Bad Request error page
    ├── 404.html           # Custom 404 Not Found error page
    └── 500.html           # Custom 500 Internal Server Error page
```

---

## Installation & Setup Instructions

### Prerequisites
- Python 3.10+ installed on your system.
- Git.

### Setup Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/alessiomanera/web-tech-lab-2026.git
   cd web-tech-lab-2026
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
   - **Windows (Command Prompt):**
     ```cmd
     python -m venv venv
     .\venv\Scripts\activate.bat
     ```
   - **macOS / Linux:**
     ```bash
     python3 -m venv venv
     source venv/bin/activate
     ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Set `FLASK_SECRET_KEY` in `.env`.
   - **Recommended for full evaluation:** set `GEMINI_API_KEY`. The AI Cultural Concierge (Module 4) is the project's core feature and runs on the Google Gemini API. Get a free key from [Google AI Studio](https://aistudio.google.com/app/apikey) (~2 minutes). With a key, the concierge performs RAG grounding on the live catalog and extracts a persistent taste profile from the conversation. The default model is `gemini-2.5-flash` (`GEMINI_MODEL`).

   > **No key = offline demo mode.** The app still starts and every other module works, but the concierge drops to a deterministic keyword-matching mode: it returns a single templated recommendation card and does **no** RAG grounding and **no** taste-profile updates. The concierge view shows a banner when this mode is active. This fallback is a deliberate network/quota safety net, not a substitute for the real concierge — evaluate with a key set.

5. **Seed the database (run once on first setup):**
   ```bash
   python seed.py
   ```

   > **Warning:** `seed.py` **drops and recreates** every table. Any bookings or accounts created since the last seed are permanently deleted. Run it once on first setup, or whenever you want a clean demo state.

   Seeding creates a demo account you can use immediately:

   | Email | Password |
   | :--- | :--- |
   | `alessio@example.com` | `password123` |

   The demo account ships with a pre-populated Cultural Taste Profile so the AI Concierge and profile dashboard are populated on first login. You may also register a fresh account at `/register`.

6. **Run the application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.

---

## Automated Test Suite

The project includes an automated test suite implemented using Python's standard library `unittest` module, running against isolated temporary SQLite databases:

```bash
# Run all 52 unit and integration tests with verbose output
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage Highlights
- **`test_database.py`:** Verifies `PRAGMA foreign_keys = ON`, unique constraints on email/booking codes, and cascading deletions.
- **`test_auth.py`:** Tests registration, Werkzeug PBKDF2 password hashing, login, session clearance on logout, and `@login_required` redirects.
- **`test_catalog.py`:** Tests multi-filtering by city/theme, search query keywords, detail pages, and the branded custom 404 page for missing experiences.
- **`test_auth.py` (redirects):** Also tests that a safe relative `?next=` target is honoured after login while an absolute off-site target is rejected (open-redirect protection).
- **`test_booking.py`:** Tests 4-step wizard rendering, date bounds (+90 days), time-slot verification, guest count bounds (1-6), and pricing calculations with add-ons.
- **`test_concierge.py`:** Tests grounded Gemini RAG mocking, recommendation card tags (`[RECOMMEND: ...]`), dynamic Markdown taste memory extraction, taste resets, and that a stored taste profile containing markup is HTML-escaped in the page.
- **`test_feedback.py`:** Tests post-visit rating submissions (enforced 1-5 range), rejection of non-numeric and out-of-range ratings, review persistence, and user ownership security.
- **`test_errors.py`:** Tests custom HTTP error pages (`400.html`, `404.html`, `500.html`) and user dashboard rendering.
