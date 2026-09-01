# Project Report — Museum Ticketing & AI Cultural Guide

**Project:** Museum Ticketing & AI Cultural Guide
**Author:** Alessio Manera (Student ID: 905639)
**Group:** Group-11 (single-person group)
**Course:** Lab of Web Technologies (AY 2025–26), Prof. Zeynep Yucel — Ca' Foscari University of Venice
**Submission date:** September 2026
**Repository:** `https://github.com/alessiomanera/web-tech-lab-2026`

---

## 1. Description and Goals

### The problem

Booking a cultural visit in Italy is fragmented and high-friction. Ticketing is spread across dozens of venue-specific portals with inconsistent flows; deciding *what* to see — given a limited time budget, a mixed-age group, or a specific interest such as Renaissance painting or Ancient Rome — is left entirely to the visitor and a pile of browser tabs. There is no single place that both sells the ticket and helps plan the visit.

### The solution

This project is a full-stack web application that does both. It presents a curated catalog of 12 bookable cultural experiences across six Italian cities (Florence, Rome, Venice, Milan, Turin, Naples), backed by 10 museums and cultural sites, and pairs it with a conversational AI concierge that recommends experiences from that same catalog and can drop a ready-to-book card directly into the chat. Recommendations are grounded in the application's own relational database rather than the model's open-ended knowledge, so the assistant only ever suggests things that actually exist and are actually bookable.

### The four modules

1. **User Authentication & Cultural Profiling** — registration and login with Flask server-side sessions and Werkzeug PBKDF2 password hashing; an account dashboard listing digital passes and past visits; a persisted Markdown "Cultural Taste Profile" that the concierge updates as the conversation reveals preferences.
2. **Experience & Museum Catalog Directory** — a dynamic catalog of experiences and museums with real-time relational filtering by city, theme, and free-text keyword search, plus per-experience detail pages covering duration, pricing, inclusions, and highlights.
3. **4-Step Ticketing & Reservation Engine** — a frictionless booking wizard: choose the package, pick add-ons, select a visit date and time slot, and receive an instant digital pass with a unique booking code. Post-visit, the user can leave a 1–5 star rating and a written review, gated to bookings they actually own.
4. **Grounded AI Cultural Concierge** — the core feature of the project. Conversational discovery powered by the Google Gemini API using Retrieval-Augmented Generation (RAG): the live `experiences` catalog is injected into the model's system instruction so it recommends only real, bookable packages, it emits an in-band `[RECOMMEND: id=…, title=…, city=…, price=…]` protocol tag that the front end parses into a real bookable card, and it writes back a structured Markdown taste profile that persists across sessions. A Gemini API key is required to run this path. **Without a key** (or if an API call fails mid-session), the concierge falls back to a deliberately limited keyword-matching mode: it matches the message against catalog cities and themes and returns a single templated recommendation card. This fallback does **not** perform RAG grounding, multi-factor reasoning, or taste-profile extraction — it exists purely as a network/quota safety net so the rest of the application stays navigable during evaluation, not as an equivalent of the real concierge.

---

## 2. How to Run the Application

### Prerequisites

- Python 3.10 or newer
- Git

### Setup

```bash
git clone https://github.com/alessiomanera/web-tech-lab-2026.git
cd web-tech-lab-2026

# Create and activate a virtual environment
python -m venv venv
# Windows (PowerShell):   .\venv\Scripts\Activate.ps1
# Windows (cmd):          .\venv\Scripts\activate.bat
# macOS / Linux:          source venv/bin/activate

pip install -r requirements.txt

# Copy the environment template
cp .env.example .env        # Windows: copy .env.example .env

python seed.py              # create and populate the database
python app.py               # start the development server
```

Then open `http://127.0.0.1:5000/`.

### Gemini API key — recommended for full evaluation

The AI Cultural Concierge (Module 4) is the project's core feature, and it runs on the Google Gemini API. **To evaluate it properly, set a key:** get a free one from [Google AI Studio](https://aistudio.google.com/app/apikey) (~2 minutes) and put it in `.env` as `GEMINI_API_KEY` (model defaults to `gemini-2.5-flash`, overridable via `GEMINI_MODEL`). With a key, the concierge does RAG grounding on the live catalog and extracts a persistent taste profile from the conversation.

**Without a key the app still starts and every other module works**, but the concierge drops to a labelled *offline demo mode*: a deterministic keyword matcher that returns one templated recommendation card and performs **no** RAG grounding and **no** taste-profile updates. The concierge view shows a banner when this mode is active. The fallback is a deliberate resilience feature (network/quota safety net), not a substitute for the real concierge.

### Demo account

`seed.py` creates a ready-to-use account with a pre-populated Cultural Taste Profile, so the booking flow, concierge, and dashboard are all populated on first login:

| Email | Password |
| :--- | :--- |
| `alessio@example.com` | `password123` |

You may also register a fresh account at `/register`.

> **Warning:** `seed.py` **drops and recreates** every table. Any accounts or bookings created since the last seed are permanently deleted. Run it once on first setup, or whenever a clean demo state is wanted.

---

## 3. Contributions and Roles

This is a **single-person group** (Group-11). Alessio Manera has **end-to-end ownership of the entire project** — every line of application code, every template, the database schema, the test suite, and all documentation were designed and written from scratch by the sole author. There are no other people involved.

For clarity, the work breaks down by workstream as follows, all performed by the same person:

| Workstream | Concrete artifacts produced |
| :--- | :--- |
| **Database & schema design** | `schema.sql` (relational DDL: `users`, `museums`, `exhibitions`, `experiences`, `tickets`; `ON DELETE CASCADE` on tickets, `ON DELETE SET NULL` on `experiences.museum_id`); `database.py` (per-request `sqlite3` connection context manager with `PRAGMA foreign_keys = ON`); `seed.py` (10 museums, 12 curated experiences across 6 cities, demo account). |
| **Backend & REST API** | `app.py` (application factory, 400/404/500 handlers); `routes.py` (page routes + `/api/book`, `/api/chat`, `/api/feedback`, `/api/profile/reset-memory`); `auth.py` (registration, login, logout, `@login_required`, safe `next` redirect handling). 100% parameterized SQL throughout. |
| **AI / RAG integration** | `_call_gemini_concierge()` in `routes.py`: RAG prompt construction grounded on the live catalog, the `[RECOMMEND: …]` in-band protocol, Markdown taste-profile extraction and persistence, and the local heuristic fallback matcher. |
| **Frontend & design system** | 13 Jinja2 templates extending `base.html`; the vanilla Neubrutalist CSS system (`variables.css`, `layout.css`, `components.css`, `utilities.css`); vanilla ES6 modules (`main.js`, `api.js`, `ui.js`, `bookingWizard.js`, `concierge.js`, `profile.js`); the anti-FOUC theme bootstrap and the light/dark toggle. |
| **QA & test suite** | `tests/` — 52 `unittest` integration tests against isolated temporary SQLite databases, covering database constraints, authentication, catalog filtering, booking arithmetic, concierge RAG and fallback, the feedback loop and its validation, and the custom error pages. |
| **Documentation** | `README.md`, `DOCS/1-Page_Project_Proposal.md`, `DOCS/Competitor_Analysis.md`, `ROADMAP.md`, `LICENSE`, and this report. |

Because there is no team to divide work across, the grading dimension of *collaboration and group structure* is satisfied here by demonstrating **complete, legible, individual authorship** of a coherent full-stack system, with a development history (30+ commits) that evidences incremental work.

---

## 4. Architecture Overview

The application uses the Flask **application-factory pattern**. `create_app(test_config=None)` builds and configures the app; passing a `test_config` lets the test suite point each test at its own throwaway SQLite file, so tests never touch a shared database.

Request lifecycle:

```
Browser
  │  HTTP request
  ▼
Flask routing  →  Blueprint view  (main_bp in routes.py  /  auth_bp in auth.py)
  │
  ▼
get_db()  →  per-request sqlite3 connection  (PRAGMA foreign_keys = ON, Row factory)
  │
  ▼
Parameterized SQL  ( ? placeholders only — no string interpolation anywhere )
  │
  ├─►  Jinja2 template render  →  HTML response   (page routes)
  └─►  jsonify(...)             →  JSON response   (/api/* routes consumed by fetch)
```

- **No ORM.** All persistence is raw `sqlite3` with parameterized queries — a deliberate choice, both to keep the data layer transparent and to match the course's emphasis on understanding SQL directly.
- **Blueprints** separate authentication (`auth_bp`) from the core application (`main_bp`).
- **Sessions** are Flask's signed cookies; `@login_required` gates the booking wizard, concierge, and profile.
- **Error handling** is centralised: `abort(404)` and unhandled errors render branded `400.html` / `404.html` / `500.html` pages.

---

## 5. Testing

```bash
python -m unittest discover -s tests -p "test_*.py" -v
```

**52 tests, all passing.** They run at integration level (real Flask test client, real SQLite) against an isolated temporary database created and destroyed per test.

| Module | What it proves |
| :--- | :--- |
| `test_database.py` | `PRAGMA foreign_keys = ON` is active per connection; `UNIQUE` constraints on email and booking code; `ON DELETE CASCADE` / `SET NULL` behave as declared. |
| `test_auth.py` | Registration, Werkzeug PBKDF2 hashing (password never stored in clear), login success/failure, session cleared on logout, `@login_required` redirects, and safe vs. rejected `?next=` redirect targets (open-redirect protection). |
| `test_catalog.py` | City / theme / keyword filtering produce the correct subset; detail pages render; a missing experience id renders the branded custom 404 page. |
| `test_booking.py` | 4-step wizard rendering, visit-date bounds, time-slot validation, guest-count bounds (1–6), and add-on pricing arithmetic. |
| `test_concierge.py` | Grounded Gemini RAG (mocked) parses `[RECOMMEND: …]` tags and persists the extracted taste profile; the offline heuristic fallback matches by city and by theme; empty messages are rejected; a stored taste profile containing markup is escaped, never rendered as HTML. |
| `test_feedback.py` | Ratings persist; reviews are gated to the owning user (404 otherwise); non-numeric ratings return 400 (not 500); ratings outside 1–5 are rejected. |
| `test_errors.py` | Custom `400.html` / `404.html` / `500.html` pages render with the correct status codes; the profile dashboard renders. |

---

## 6. Security Measures

| Measure | Implementation |
| :--- | :--- |
| **SQL injection** | 100% parameterized queries (`?` placeholders) — verified across every statement in `routes.py`, `auth.py`, `database.py`, `seed.py`. No f-string or `%`-formatted SQL anywhere. |
| **Password storage** | Werkzeug `generate_password_hash` / `check_password_hash` (PBKDF2-SHA256, per-user salt). Plaintext passwords are never stored or logged. |
| **Authentication & authorisation** | Flask signed-cookie sessions; `@login_required` on the booking wizard, concierge, and profile; feedback writes verify `user_id` ownership of the target booking. |
| **Server-side output escaping** | Jinja2 autoescaping on all templates. The one former `\|safe` filter on user-controlled taste-profile text was removed and replaced with plain interpolation plus a CSS `white-space: pre-line` class. |
| **Client-side output escaping** | `concierge.js` escapes every HTML-significant character in user chat input, model output, and the stored taste profile before it reaches the DOM (`escapeHtml`; taste profile written via `textContent`, not `innerHTML`). This closes a reflected/stored XSS vector in the chat renderer. |
| **Open-redirect protection** | The post-login `?next=` target is accepted only if it is a same-site relative path; absolute URLs and protocol-relative `//` targets are discarded and the user is sent to the home page. |
| **Booking-code collisions** | Booking codes are `EXP-2026-` + 6 random alphanumerics on a `UNIQUE` column; insertion retries on the rare `IntegrityError` instead of surfacing a 500. |

---

## 7. Known Limitations and Future Work

Honest scope boundaries of the delivered system:

- **The concierge is single-turn.** No running conversation history is sent to Gemini; continuity between messages is carried only by the persisted Cultural Taste Profile. A true multi-turn history buffer is future work.
- **RAG grounding covers the `experiences` table only** — the 12 bookable packages. It does not ground on `museums` or `exhibitions`, and does not know venue logistics such as street addresses, general opening hours, or physical accessibility.
- **No payment integration.** Booking issues a digital pass and a booking code; no money changes hands.
- **No capacity or inventory model.** Time slots never sell out; there is no per-slot seat count.
- **Not a production deployment.** SQLite and the Flask development server are appropriate for the assignment and local evaluation, not for production traffic.
- **Responsive coverage** is targeted at desktop and tablet; narrow-phone layouts are usable but lightly tested.

Planned work: QR-code rendering on digital passes, `.ics` calendar export for booked slots, a multi-turn conversation buffer for the concierge, grounding extended to museums and exhibitions, and a real seat-capacity model.
