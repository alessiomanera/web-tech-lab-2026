# Project Implementation Roadmap

This document serves as the master source of truth and historical tracking timeline for the **Museum Ticketing & AI Cultural Guide** web application. It documents past completed milestones, current active development, and future implementations organized into detailed phases and subtasks.

---

## Phase 1: Foundation, Academic Guidelines & Planning
- [x] **Review Academic Requirements & Evaluation Criteria**
  - [x] Analyze the official course project guide (`AY2025_2026_project_guide.pdf`, distributed on Moodle) — 30+1 grading rubric: Code Quality, Innovation, UX/UI, Deployment, Collaboration, Presentation, Course Knowledge.
  - [x] Confirm single-person group structure (Group-11 created by Professor Yucel; solo work declared 25 Jun 2026).
  - [x] Identify the guide's recommended technology stack (HTML5, Vanilla CSS, Vanilla JavaScript, Python 3 / Flask) and choose the rest — SQLite, no ORM, Google Gemini — ourselves, since the guide leaves the data layer and any extra integrations to the student.

### Confirmed Academic Milestones (Sep 11, 2026 exam session)

| Milestone | Status | Detail |
| :--- | :--- | :--- |
| Group members declared | [x] Done | Group-11 created by professor (25 Jun 2026). |
| 1-page proposal submitted on Moodle | [x] Done | Uploaded 24 Aug 2026 (`PROJECT_PROPOSAL.pdf`). |
| Professor proposal feedback | [x] Received | 22 Aug 2026 — approved, **no revisions requested**. |
| Exam registration / booking | [x] Confirmed | Booked for Sep 11, 2026. |
| **Project archive on Moodle** | [ ] **Due Sep 4, 23:55 (guide) / 23:59 (professor email)** | Target: well before Sep 4. |
| Written exam | [ ] Sep 11, 10:00 (~40 min) | 5 multiple-choice + 3 open-ended; **scope = lecture slides**. |
| Oral project presentation | [ ] Sep 11, ~11:00 (~30 min) | May be asked to stay as witness for another group. |

- [x] **Repository Setup & Modular Directory Skeleton**
  - [x] Initialize Git repository with `testing` development branch workflow.
  - [x] Create standardized project hierarchy: `/templates/`, `/static/css/`, `/static/js/`, `/static/images/`, `/DOCS/`, `/instance/`.
  - [x] Configure virtual environment (`venv`) and initial `requirements.txt` (`Flask`, `python-dotenv`, `google-generativeai`).
  - [x] Configure environment variables template (`.env.example`) and security ignores (`.gitignore`).
- [x] **Draft Project Proposal (`DOCS/1-Page_Project_Proposal.md`)**
  - [x] Formulate project purpose and dual core objectives (Ticketing + AI Concierge).
  - [x] Identify primary target audiences (tourists, families, cultural sites).
  - [x] Define the 4 core system modules (User Management, Catalog Directory, Ticketing Engine, AI Concierge).
  - [x] Define task distribution and roles for single-member delivery (Alessio Manera, ID: 905639).
  - [x] Ensure strict 1-page A4 PDF length constraint for Moodle submission.
- [x] **Coding Guidelines & Documentation Standards**
  - [x] Author comprehensive project overview and coding standards (`README.md`).
  - [x] Compile detailed market and competitor analysis report (`DOCS/Competitor_Analysis.md`).
  - [x] Synthesize course guidelines, exam rules, and architectural constraints (internal working notes).
- [x] **Submit 1-Page Proposal to Professor on Moodle**
  - [x] Generate clean A4 PDF from `DOCS/1-Page_Project_Proposal.md` (`PROJECT_PROPOSAL.pdf`, emailed 19 Aug 2026).
  - [x] Submit on Moodle before the proposal deadline (uploaded 24 Aug 2026).
  - [x] Review professor feedback — approved 22 Aug 2026 with **no revision requests**; no adjustments required.

---

## Phase 2: Design System & Neubrutalism Architecture
- [x] **Core Design Tokens (`static/css/variables.css`)**
  - [x] Stark high-contrast light theme (`#FFFFFF` background, `#000000` text & borders).
  - [x] Strict Neubrutalism geometry: `3px` solid borders, `4px 4px 0px 0px` hard drop-shadows, `0px` border-radius.
  - [x] Purposeful accent highlights for actions, badges, and focus indicators.
  - [x] Typography: Strictly `Inter` sans-serif with aggressive font weights (800/900).
- [x] **Layout & Responsive Grid (`static/css/layout.css`)**
  - [x] Mobile-first layout with CSS Grid and Flexbox containers.
  - [x] Custom tactile SVG cursor implementation (`cursor.svg`, `cursor-pointer.svg`).
- [x] **Modular Component Library & Micro-interactions**
  - [x] Mechanical button click press states (`translate(4px, 4px)` with shadow collapse).
  - [x] Style UI components: Neubrutalist cards, badges, inputs, alerts, navigation bars (`static/css/components.css`).
  - [x] Create helper classes and utilities (`static/css/utilities.css`).
- [x] **Accessibility & Performance Standards**
  - [x] Ensure WCAG AA contrast ratio compliance across all text and interactive elements (with AAA compliance on solid black body text). Re-verified 2026-09-02 by measuring rendered colours against composited backgrounds across every page in both themes: 0 failing pairs.
  - [x] Set explicit dimensions / aspect-ratios on images to guarantee zero Cumulative Layout Shift (CLS).

---

## Phase 3: Frontend Templates & Client-Side Scripts (Experience Economy UI)
- [x] **Base Layout Template (`templates/base.html`)**
  - [x] Establish HTML5 semantic structure (`<header>`, `<nav>`, `<main>`, `<footer>`).
  - [x] User-centric navigation: `Home`, `Explore Experiences`, `Tailor Experience (AI)`, `Book Now`, `My Experiences`.
  - [x] Render server-side flash messages as Neubrutalist alert boxes on the authentication forms (`login.html`, `register.html`).
- [x] **Experience Economy Page Templates**
  - [x] `templates/index.html`: Landing page with hero banner, 3-step value workflow, and trending packages.
  - [x] `templates/experiences.html`: Full 12-Experience catalog with search bar, city/theme filter pills, and Standard/Compact view switcher with `localStorage` persistence.
  - [x] `templates/experience_detail.html`: Deep-dive view with full itinerary, included perks, and customizable add-ons.
  - [x] `templates/booking.html`: 4-step wizard (Package & Add-ons $\rightarrow$ Date & Slot $\rightarrow$ Summary $\rightarrow$ Digital Pass).
  - [x] `templates/guide.html`: AI Cultural Concierge with grounded RAG, in-chat booking cards, and live Markdown taste memory panel.
  - [x] `templates/profile.html`: User dashboard with active digital passes, visit review/feedback loops, and taste memory inspector.
  - [x] `templates/login.html` & `templates/register.html`: Neubrutalist authentication forms.
- [x] **Client-Side Interactions (`static/js/main.js`, `static/js/bookingWizard.js`)**
  - [x] 4-step wizard state machine and dynamic addon price calculations.
  - [x] Time-slot selection and date bounding (today to +90 days).
  - [x] Asynchronous feedback and review submission handlers.

---

## Phase 4: Backend Setup & SQLite Database Schema
- [x] **Flask Application Factory Architecture (`app.py`)**
  - [x] Implement `create_app()` factory pattern for clean lifecycle management.
  - [x] Configure SQLite URI (`instance/app.db`) and secret keys via `python-dotenv`.
  - [x] Register Blueprints (`main_bp` in `routes.py`, `auth_bp` in `auth.py`).
  - [x] Initialize database connections using raw standard library `sqlite3` (`database.py`).
- [x] **Relational Database Schema Definition (`schema.sql`)**
  - [x] Define clean DDL schema with proper FOREIGN KEY constraints and PRAGMA foreign_keys = ON.
  - [x] Table `users`: `id`, `name`, `email` (unique), `password_hash`, `preferences` (Markdown Taste Memory).
  - [x] Table `museums`: `id`, `name`, `description`, `location`, `city`, `image_url`.
  - [x] Table `experiences`: `id`, `title`, `tagline`, `city`, `theme`, `duration_minutes`, `base_price`, `badge`, `included_items_json`, `available_addons_json`, `highlights`, `museum_id`.
  - [x] Table `tickets`: `id`, `booking_code`, `user_id`, `experience_id`, `visit_date`, `time_slot`, `guests_count`, `selected_addons_json`, `total_price`, `status`, `feedback_rating`, `feedback_text`.
- [x] **Database Seeding (`seed.py`)**
  - [x] Populate SQLite database with **Top 12 Curated Italian Cultural Experiences** across 6 major art cities (Florence, Rome, Venice, Milan, Turin, Naples).
  - [x] Seed 12 baseline cultural institutions (one per curated experience) and a sample user account with an initialized Markdown Taste Profile.

---

## Phase 5: Dynamic Integration & Authentication
- [x] **User Authentication & Session Management (`auth.py`)**
  - [x] Registration handler (`/register` POST) with secure password hashing via `werkzeug.security.generate_password_hash`.
  - [x] Login handler (`/login` POST) with password verification via `check_password_hash`.
  - [x] Session establishment (`session['user_id']`) and logout handler (`/logout`).
  - [x] Route protection via `@login_required` decorator (`/booking`, `/concierge`, `/profile`).
- [x] **Dynamic Catalog & Booking Workflows (`routes.py`)**
  - [x] Query and render 12 experiences with search and city filter on `/experiences`.
  - [x] 4-step wizard endpoint `/booking` with support for URL preselection (`?exp_id=X` or `?museum_id=Y`).
  - [x] Booking submission handler (`POST /booking`): validate input server-side, compute total with add-ons, insert row in `tickets`, and show a real digital confirmation pass.
  - [x] Feedback submission endpoint (`POST /api/feedback`).

---

## Phase 6: AI Cultural Concierge & Grounded RAG Feature
- [x] **Gemini API Integration & Grounding Workflow**
  - [x] Configure Google Generative AI SDK (`google-generativeai`) with secure `GEMINI_API_KEY`.
  - [x] Ground system prompt directly on the 12 SQLite experiences to eliminate hallucinations.
  - [x] In-chat actionable booking card triggers (`[RECOMMEND: id=X, title="Y", city="Z", price=W]`).
- [x] **Dynamic Markdown Taste Memory Pipeline (`routes.py`, `templates/guide.html`)**
  - [x] Background preference extraction: automatically updates `preferences` column in `users` table as structured Markdown after each conversation.
  - [x] Live Taste Memory side panel in chat view and user dashboard (`/profile`).
  - [x] Option to reset/refine taste memory on demand (`POST /api/profile/reset-memory`).

---

## Phase 7: Quality Assurance, Security, & Testing
- [x] **Code Quality & Modularity Audit (6 Points Academic Evaluation)**
  - [x] Verify adherence to DRY principles across Python blueprints, Jinja2 templates, and CSS stylesheets.
  - [x] Add comprehensive docstrings and inline comments across all functions and route handlers.
  - [x] Ensure consistent code formatting and PEP 8 compliance for backend Python files.
- [x] **Automated Test Suite Scaffold & Execution**
  - [x] Built comprehensive 52-test automated test suite using Python standard library `unittest`.
  - [x] Isolated test databases with full foreign key constraint checks (`test_database.py`).
  - [x] Authentication and PBKDF2 hashing verification (`test_auth.py`).
  - [x] Catalog search and multi-filtering tests (`test_catalog.py`).
  - [x] 4-Step booking engine validation, bounds, and arithmetic tests (`test_booking.py`).
  - [x] Grounded Gemini RAG, recommendation cards, and dynamic taste memory tests (`test_concierge.py`).
  - [x] Post-visit review loops and user ownership verification (`test_feedback.py`).
  - [x] Custom HTTP error pages and profile dashboard tests (`test_errors.py`).
- [x] **Security & Error Handling Verification**
  - [x] Verify SQL injection protection via raw SQLite3 parameterized queries.
  - [x] Verify Cross-Site Scripting (XSS) prevention via Jinja2 auto-escaping.
  - [x] Verify secure password storage (Werkzeug SHA-256 / PBKDF2).
  - [x] Implement custom HTTP error pages (`400.html`, `404.html`, `500.html`).

- [x] **Pre-Submission Security & Validation Hardening (Sep 2026)**
  - [x] Close a reflected/stored XSS vector in the AI Concierge chat renderer: extract the inline `<script>` into `static/js/concierge.js`, escape all user input, model output, and stored taste-profile text before it reaches the DOM, and remove the dead `|safe`-filtered session history block.
  - [x] Extract the profile dashboard inline `<script>` into `static/js/profile.js`; route both new modules through the previously-unused `static/js/api.js` fetch layer.
  - [x] `/api/feedback`: return HTTP 400 (not 500) on non-numeric ratings and reject ratings outside the 1–5 range; use timezone-aware timestamps.
  - [x] Render the branded custom 404 page for missing experiences via `abort(404)` instead of plain text.
  - [x] Make booking codes collision-safe: 6-character suffix with retry on the `UNIQUE` constraint.
  - [x] Honour a safe relative `?next=` redirect after login; reject absolute/off-site targets (open-redirect protection).
  - [x] Correct the Gemini model identifier; log the local-fallback path instead of silently swallowing the exception. (Superseded 2026-09-02: `gemini-2.5-flash` was retired by Google and began returning `404 — no longer available to new users`. The default is now the `gemini-flash-lite-latest` alias, with `gemini-3.6-flash` as a verified fallback.)
  - [x] Reframe the AI Concierge: the Gemini RAG path is the core feature (requires `GEMINI_API_KEY`); the keyword-matching fallback is a labelled resilience safety net that does no RAG and no taste-profile updates. `/api/chat` now returns an `offline` flag and the concierge view shows a yellow banner when the fallback is active. Docs (README, project report) updated to match.
  - [x] Replace the last deprecated `datetime.utcnow()` (in `seed.py`) with timezone-aware `datetime.now(timezone.utc)`.

- [x] **Final Pre-Submission Audit (2026-09-02)** — a full re-verification against the live code, a throwaway clone, a real browser, and a live Gemini key.
  - [x] **Gemini model:** `gemini-2.5-flash` was retired by Google mid-project and returns `404 — no longer available to new users`; it is still listed by `list_models()`, so only a real `generateContent` call exposes it. The default is now `gemini-flash-lite-latest` with `gemini-3.6-flash` as a measured-working fallback. (The previously-hardcoded `gemini-flash-latest` fallback was also found unusable — two consecutive `504 Deadline expired` after ~300 s.)
  - [x] **Server-side pricing integrity:** `create_booking()` trusted the add-on prices sent in the request, so a crafted `POST /api/book` could confirm a €62.00 booking for €2.00. Add-ons are now re-resolved against the experience's own catalog entry; two regression tests cover it.
  - [x] **Responsive:** fixed a dead `@media (max-width: 900px)` rule for `.profile-layout` (placed above the base rule, so it lost on source order) and the intrinsic `min-width` floors that overflowed the concierge and the card grids on narrow phones.
  - [x] **Contrast:** introduced darkened text variants of the accent colours (`--primary-text`, `--accent-text`, `--accent-yellow-text`) and `--on-accent` for text on a coloured fill. Rendered-pixel audit went from 25 failing pairs in light mode and 15 in dark to **0 in both**.
  - [x] **Keyboard:** booking time slots were non-focusable `<div>`s; they are now `<button>` elements with `aria-pressed` and a matching focus ring.
  - [x] **Booking wizard:** clicking an add-on's `<label>` toggled the checkbox twice and cancelled itself out, so the add-on never applied.
  - [x] **Error handling:** `app.run(debug=True)` was unconditional, and Flask's debugger replaces the registered error handlers — so the branded `500.html` never rendered. Debug is now opt-in via `FLASK_DEBUG=1`.
  - [x] Removed three dead references (an unused `flash` import, an unused `MagicMock` import, and a `WTF_CSRF_ENABLED` test-config key for a library the project does not depend on).
  - [x] Confirmed clean: 100% parameterized SQL across all 33 call sites, Jinja2 autoescaping intact, client-side escaping probed with a live XSS payload, complete `@login_required` coverage, the `?next=` open-redirect guard, no secrets in any commit, and a fresh clone that runs from `README.md` verbatim.

- [x] **Audit Follow-Up: the deferred findings, closed (2026-09-02)** — the seven items the audit had parked as "acceptable, but be ready to explain".
  - [x] **CSRF protection**, implemented directly rather than by adding Flask-WTF, so the mechanism stays legible in the codebase: a per-session token from `secrets.token_urlsafe(32)`, compared with `secrets.compare_digest`, carried as a hidden `csrf_token` field on the HTML forms and an `X-CSRFToken` header on the JSON endpoints, enforced by a single `before_request` hook. The session cookie is now explicitly `HttpOnly` and `SameSite=Lax` as a second layer instead of relying on a browser default. Seven regression tests cover missing, forged and valid tokens on both surfaces.
  - [x] **Museum foreign keys:** added Musei Vaticani and the Museo Archeologico Nazionale di Napoli as seeded institutions, so all 12 experiences now resolve to their own venue (previously those two borrowed another same-city venue's id). No city mismatches remain and every museum has a bookable experience.
  - [x] **Taste profile presentation:** the concierge's live memory panel showed raw Markdown (`### …`, `- **Label:**`) while the dashboard showed it parsed. Both now render the same label/value rows — server-side through `_parse_taste_profile()`, client-side through a mirrored `parseTasteProfile()` in `concierge.js`.
  - [x] **Chat formatting:** the renderer only understood `**bold**`, so the model's `*italic*` and `***bold italic***` leaked literal asterisks into the reply. It now handles all three (longest-delimiter-first, on already-escaped text), and the system instruction asks the model to stay within that subset.
  - [x] **`.btn-success`:** the booking wizard's confirm button carried a class no stylesheet defined. Defined it against `--success-color`, so the one irreversible step reads differently from every other coral CTA.
  - [x] **Dead CSS removed:** six unreferenced rules (`.card-clickable`, `.cta-button-yellow`, `.cta-button-blue-sm`, `.text-accent-color`, `.side-card-title`, `.mt-4`, plus `.preserve-lines` once the taste panel stopped needing it) and six unread custom properties. `.sr-only` was kept deliberately as a standard accessibility utility.
  - [x] **`_current_user(db)`:** collapsed the session-user lookup that was repeated identically in four route handlers.

- [x] **Cross-Device & Responsive Usability Testing**
  - [x] Validate responsive layout at 320 / 375 / 768 / 1440px across all seven pages — no horizontal overflow at any width. The profile dashboard stacks to one column below 900px (the media query was initially placed above the base `.profile-layout` rule and lost on source order; corrected 2026-09-02).
  - [x] Verify keyboard navigation and screen-reader accessibility. Booking time slots are real `<button>` elements with `aria-pressed`, reachable and operable by keyboard (they were non-focusable `<div>`s until 2026-09-02).
  - [x] Verify zero visual regressions or layout shifts during dynamic interactions.
- [x] **Experience Catalog & Asset Fidelity Audit (1-by-1 Insertion Check)**
  - [x] Individually inspect each of the 12 cultural experience entries in `seed.py` and the SQLite database.
  - [x] Replace any mismatched or generic placeholder imagery with verified, authentic local stock photos across all 12 museums and 12 experiences (`/static/images/museums/` and `/static/images/experiences/`).
  - [x] Cross-check all 12 experiences for accurate city landmarks, durations, transparent pricing, highlight tags, and museum foreign key integrity — every experience now resolves to its own venue, with no city mismatches (the Vatican and MANN packages previously borrowed another same-city venue's id; Musei Vaticani and the Museo Archeologico Nazionale di Napoli were added as seeded institutions 11 and 12).

---

## Phase 8: Final Packaging, Documentation & Exam Presentation
- [x] **Project Setup & Run Documentation**
  - [x] Finalize `README.md` with complete, step-by-step instructions for running the project locally.
  - [x] Verify virtual environment activation commands for Windows (`powershell`), macOS, and Linux.
  - [x] Ensure all dependencies are locked in `requirements.txt`.
- [x] **Oral Presentation Preparation & Architecture Defense**
  - [x] Structure presentation outline and 5-minute live demonstration walkthrough.
  - [x] Align implementation details with technical evaluation criteria.
  - [x] Document technical architecture, SQL parameterization, RAG grounding, and Neubrutalism design rationale.
  - [x] **High-Contrast Light/Dark Theme System (shipped in `e5c499f`):** canonical Neubrutalist palette (Coral Red `#FF6B6B`, Sky Blue `#74B9FF`, Bold Yellow `#FFD23F`, Soft Green `#88D498`) with a header toggle, `localStorage` persistence, SVG sun/moon icons, and an anti-FOUC bootstrap script in `<head>`.
  - [x] Document known scope boundaries (not part of any further development plan — see `DOCS/PROJECT_REPORT.md` §7):
    - **Digital passes** render no QR code and export to no calendar format.
    - **The concierge is single-turn** — no running conversation history is sent to Gemini; only the persisted taste profile carries context.
    - **RAG grounding covers the `experiences` table only**, not `museums` or `exhibitions`.
- [ ] **Moodle Submission Packaging**
  - [ ] Clean temporary files, caches (`__pycache__`, `.pytest_cache`), and non-essential folders prior to bundling.
  - [ ] Package final archive (`.zip`) containing the source code, SQLite database seed, and documentation document as requested in the project guide.
  - [ ] Submit on Moodle ahead of the deadline.
