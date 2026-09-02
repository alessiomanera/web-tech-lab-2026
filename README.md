# Museum Ticketing & AI Cultural Guide

**Author:** Alessio Manera (Student ID: 905639)  
**Course:** Lab of Web Technologies (AY 2025/26)  
**Group:** Group-11 (single-person group)

A full-stack web application for discovering and booking tickets to museums and cultural sites in Italy, paired with an AI cultural concierge. The concierge runs on Google Gemini using Retrieval-Augmented Generation over the application's own SQLite catalog, so it only ever recommends experiences that exist and can actually be booked.

> **Full documentation is in [`DOCS/PROJECT_REPORT.md`](DOCS/PROJECT_REPORT.md)** (also provided as a PDF). It covers the goals, architecture, contributions, testing, security measures, and known limitations. This README is the short version: what it is, and how to run it.

---

## Stack

| Layer | Choice |
| :--- | :--- |
| Frontend | Semantic HTML5 with Jinja2 template inheritance; vanilla CSS3 (custom Neubrutalist design system, no framework); vanilla JavaScript, ES6+ syntax, loaded as classic deferred scripts with no bundler |
| Backend | Python 3 and Flask, application-factory pattern, two Blueprints (`routes.py`, `auth.py`) |
| Database | Raw SQLite3 with parameterized queries via the standard library `sqlite3`. No ORM. Tables: `users`, `museums`, `exhibitions`, `experiences`, `tickets` |
| AI | Google Gemini (`gemini-flash-lite-latest`, set via `GEMINI_MODEL`) through the `google-generativeai` SDK, with RAG grounding on the live `experiences` catalog |
| Tests | 61 integration tests using the standard library `unittest` |

---

## Quick start

Requires Python 3.10 or newer. Git is only needed if you are cloning; if you already have this as a folder, start at step 2 from inside it.

```bash
# 1. Get the code
git clone https://github.com/alessiomanera/web-tech-lab-2026.git
cd web-tech-lab-2026

# 2. Create and activate a virtual environment
python -m venv venv
#    Windows (PowerShell):  .\venv\Scripts\Activate.ps1
#    Windows (cmd):         .\venv\Scripts\activate.bat
#    macOS / Linux:         source venv/bin/activate
#    Your prompt should now start with "(venv)".

# 3. Install dependencies (3 packages: Flask, python-dotenv, google-generativeai)
pip install -r requirements.txt

# 4. Create your .env from the template
cp .env.example .env        # Windows: copy .env.example .env

# 5. Create and populate the database (run once)
python seed.py

# 6. Run
python app.py               # then open http://127.0.0.1:5000/
```

**Demo account:** `alessio@example.com` / `password123`

> `seed.py` drops and recreates every table. Anything created since the last seed is permanently deleted.

### Two things that commonly trip up a first run

- **PowerShell says "running scripts is disabled on this system".** Run `Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass` once in that same terminal, then retry the activate line. It only affects that one window.
- **"Address already in use" on port 5000.** Common on macOS, where AirPlay Receiver claims it. Either free the port, or run on another one: `python -c "from app import create_app; create_app().run(port=5001)"`.

### Gemini API key (recommended)

The concierge is the core feature, and it needs a key to do real RAG grounding. Get one free at [Google AI Studio](https://aistudio.google.com/app/apikey) (about two minutes, no credit card), then paste it into `.env` as `GEMINI_API_KEY=`.

Without a key the app still starts and every other module works, but the concierge drops to a labelled offline mode: a keyword matcher returning one templated card, with no RAG grounding and no taste-profile updates. It is a safety net for network and quota failures, not an equivalent of the real concierge.

`FLASK_SECRET_KEY`, the other setting in `.env`, signs session cookies. The placeholder is fine for local evaluation and does not need changing.

---

## Tests

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

61 tests, all passing. They run at integration level against an isolated temporary SQLite database created and destroyed per test, covering database constraints, authentication and CSRF, catalog filtering, booking and pricing arithmetic, the concierge's RAG and fallback paths, the feedback loop, and the custom error pages. Per-module detail is in section 5 of the project report.

---

## Layout

```text
app.py            # application factory and entry point
database.py       # per-request SQLite connection, PRAGMA foreign_keys = ON
schema.sql        # table definitions
routes.py         # main Blueprint: pages plus /api/book, /api/chat, /api/feedback
auth.py           # auth Blueprint: register, login, logout, @login_required
seed.py           # populates 12 museums, 12 experiences, demo account
templates/        # 13 Jinja2 templates, all extending base.html
static/css/       # variables, layout, components, utilities
static/js/        # main, api, ui, bookingWizard, concierge, profile
tests/            # 61 unittest integration tests
DOCS/             # project report, 1-page proposal, competitor analysis
ROADMAP.md        # phased development log
```

---

## Licence

MIT. See [`LICENSE`](LICENSE).
