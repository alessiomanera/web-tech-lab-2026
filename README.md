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
- **Database & Storage:** Raw SQLite3 using parameterized queries (Python standard library `sqlite3`), no ORM helper libraries (`database.py`, `schema.sql`: `users`, `museums`, `exhibitions`, `experiences`, `tickets`). The `exhibitions` table is seeded with sample data but not yet surfaced by any route, template, or the concierge's RAG grounding — see Known Limitations in `DOCS/PROJECT_REPORT.md`.
- **AI Engine (Module 4, core feature):** Google Gemini API (`gemini-flash-lite-latest`, configurable via `GEMINI_MODEL`) via the official `google-generativeai` SDK, implementing Retrieval-Augmented Generation (RAG) over the `experiences` SQLite catalog with persistent taste-profile extraction. Requires `GEMINI_API_KEY`. A deterministic keyword-matching fallback (no RAG, no profile updates) keeps the app usable without a key or during an API outage — a labelled safety net, not an equivalent path.

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
- **Accessibility:** WCAG AA contrast across every rendered text/background pair in both themes (verified by measuring computed colours against composited backgrounds on all pages, not by inspecting the stylesheet); AAA on body text. Accent colours have separate darkened variants (`--primary-text`, `--accent-text`, `--accent-yellow-text`) for text on the page ground, while text on a coloured fill is black (`--on-accent`). No horizontal scrolling at 320px (WCAG 1.4.10 Reflow), and zero Cumulative Layout Shift (CLS).

---

## Project Structure

```text
web-tech-lab-2026/
├── app.py                 # Application factory and entry point
├── database.py            # SQLite connection context manager & initialization
├── schema.sql             # SQL database definition (tables for users, museums, exhibitions, experiences, tickets)
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
- Git — only needed for Step 1 if you're cloning. If you already have the project as a folder (e.g. unzipped from a Moodle submission), skip Git entirely.
- An internet connection (to install dependencies in Step 3, and optionally to reach the Gemini API in Step 4).

### Setup Steps
1. **Get the code.**
   - **Cloning from GitHub:**
     ```bash
     git clone https://github.com/alessiomanera/web-tech-lab-2026.git
     cd web-tech-lab-2026
     ```
   - **Already have it as a folder or a `.zip`?** Extract it if needed, then open a terminal *inside* that folder (the one containing `app.py`) and skip straight to Step 2.

2. **Create and activate a virtual environment.** A virtual environment is a private, isolated copy of Python for this project only — it keeps this project's dependencies from clashing with anything else on your machine, and nothing here touches your system-wide Python.
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
     > **If you see "running scripts is disabled on this system":** PowerShell blocks script execution by default on many machines. Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in the same terminal — this only changes the policy for this one terminal window, not your whole system — then retry the `Activate.ps1` line above.
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
   - **How do I know it worked?** Your terminal prompt now starts with `(venv)`. If you close and reopen the terminal, you'll need to run the *activate* line again (not the whole setup) before continuing.

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
   This installs exactly three packages (`Flask`, `python-dotenv`, `google-generativeai`) — everything else the app uses is Python's own standard library.

4. **Configure environment variables.** This project reads its secrets and settings from a file named `.env`, which you create by copying the provided template:
   - **macOS / Linux / Git Bash:**
     ```bash
     cp .env.example .env
     ```
   - **Windows (Command Prompt or PowerShell):**
     ```cmd
     copy .env.example .env
     ```
   - Open the new `.env` file in any text editor. It has two settings:
     - **`FLASK_SECRET_KEY`** — signs login session cookies. **You do not need to change this to run or evaluate the project** — the placeholder value works fine locally. (It only matters for a real internet-facing deployment; see the comment inside `.env.example` if you're curious.)
     - **`GEMINI_API_KEY`** — **recommended for full evaluation.** The AI Cultural Concierge (Module 4) is the project's core feature and runs on the Google Gemini API. Without a real key here, the concierge still works, but in a deliberately limited fallback mode (see the box below).

     **To get a free key (about 2 minutes, no credit card):**

     1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey) and sign in with any Google account.
     2. Click **Create API key** (or **Get API key** → **Create API key**).
     3. Copy the key it shows you.
     4. Paste it into `.env` in place of `your_gemini_api_key_here`, so the line reads `GEMINI_API_KEY=AIza...` (your actual key).
     5. Save the file. No restart needed yet — you haven't started the server.

     With a key, the concierge performs RAG grounding on the live catalog and extracts a persistent taste profile from the conversation. The default model is `gemini-flash-lite-latest` (`GEMINI_MODEL`); if it is unavailable the client falls back to `gemini-3.6-flash` before dropping to offline mode.

   > **No key = offline demo mode.** The app still starts and every other module works, but the concierge drops to a deterministic keyword-matching mode: it returns a single templated recommendation card and does **no** RAG grounding and **no** taste-profile updates. The concierge view shows a banner when this mode is active. This fallback is a deliberate network/quota safety net, not a substitute for the real concierge — evaluate with a key set.

5. **Seed the database (run once on first setup):**
   ```bash
   python seed.py
   ```
   You should see output ending in `Database successfully seeded with Top 12 Experiences and demo user!` — that confirms it worked. (`instance/app.db` is created automatically; you don't need to create any folder or file yourself.)

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
   You should see Flask log a line like `Running on http://127.0.0.1:5000`. Open your browser and navigate to `http://127.0.0.1:5000/`.

   > **Port 5000 already in use / "Address already in use"?** Something else on your machine is using that port (on recent macOS, it's often the AirPlay Receiver). Either free port 5000 (macOS: System Settings → General → AirDrop & Handoff → turn off AirPlay Receiver), or run the app on a different port: `python -c "from app import create_app; create_app().run(port=5001)"`, then open `http://127.0.0.1:5001/` instead.

   > Debug mode (Werkzeug's interactive debugger and auto-reload) is opt-in and off by default, so the branded `500.html` error page always renders. Enable it with `FLASK_DEBUG=1 python app.py` (PowerShell: `$env:FLASK_DEBUG=1; python app.py`) if you need tracebacks while developing.

### If something doesn't work

| Symptom | Likely cause | Fix |
| :--- | :--- | :--- |
| `ModuleNotFoundError: No module named 'flask'` | The virtual environment isn't active in this terminal | Re-run the *activate* line from Step 2 (your prompt should show `(venv)`) |
| PowerShell: "running scripts is disabled on this system" | Windows' default script-execution policy | See the box under Step 2 |
| `Address already in use` when running `python app.py` | Another program is already using port 5000 | See the box under Step 6 |
| Concierge shows a yellow "offline mode" banner | No valid `GEMINI_API_KEY` in `.env`, or it's still the placeholder | Follow the 5 numbered steps under Step 4 to get a free key |
| Login fails with the demo account | The database was never seeded, or was reseeded after you registered a different account | Re-run `python seed.py`, then log in with `alessio@example.com` / `password123` |

---

## Automated Test Suite

The project includes an automated test suite implemented using Python's standard library `unittest` module, running against isolated temporary SQLite databases:

```bash
# Run all 61 unit and integration tests with verbose output
python -m unittest discover -s tests -p "test_*.py" -v
```

### Test Coverage Highlights
- **`test_database.py`:** Verifies `PRAGMA foreign_keys = ON`, unique constraints on email/booking codes, and cascading deletions.
- **`test_auth.py`:** Tests registration, Werkzeug PBKDF2 password hashing, login, session clearance on logout, `@login_required` redirects, and CSRF protection (a POST with a missing or forged token is rejected on both the HTML forms and the JSON API, while GET requests are untouched).
- **`test_catalog.py`:** Tests multi-filtering by city/theme, search query keywords, detail pages, and the branded custom 404 page for missing experiences.
- **`test_auth.py` (redirects):** Also tests that a safe relative `?next=` target is honoured after login while an absolute off-site target is rejected (open-redirect protection).
- **`test_booking.py`:** Tests 4-step wizard rendering, date bounds (+90 days), time-slot verification, guest count bounds (1-6), and pricing calculations with add-ons.
- **`test_concierge.py`:** Tests grounded Gemini RAG mocking, recommendation card tags (`[RECOMMEND: ...]`), dynamic Markdown taste memory extraction, taste resets, and that a stored taste profile containing markup is HTML-escaped in the page.
- **`test_feedback.py`:** Tests post-visit rating submissions (enforced 1-5 range), rejection of non-numeric and out-of-range ratings, review persistence, and user ownership security.
- **`test_errors.py`:** Tests custom HTTP error pages (`400.html`, `404.html`, `500.html`) and user dashboard rendering.
