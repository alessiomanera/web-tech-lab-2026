# Project Implementation Roadmap

This document serves as the master source of truth and historical tracking timeline for the **Museum Ticketing & AI Cultural Guide** web application. It documents past completed milestones, current active development, and future implementations organized into detailed phases and subtasks.

---

## Phase 1: Foundation, Academic Guidelines & Planning
- [x] **Review Academic Requirements & Evaluation Criteria**
  - [x] Analyze `AY2025_2026_project_guide.pdf` (30+1 grading rubric: Code Quality, Innovation, UX/UI, Deployment, Collaboration, Presentation, Course Knowledge).
  - [x] Confirm single-person group structure (Group-11 registered with Professor Yucel).
  - [x] Identify required technology stack (HTML5, Vanilla CSS, Vanilla JavaScript, Python 3 / Flask, SQLite).
- [x] **Repository Setup & Modular Directory Skeleton**
  - [x] Initialize Git repository with `testing` development branch workflow.
  - [x] Create standardized project hierarchy: `/templates/`, `/static/css/`, `/static/js/`, `/static/images/`, `/DOCS/`, `/instance/`.
  - [x] Configure virtual environment (`venv`) and initial `requirements.txt` (`Flask`, `Flask-SQLAlchemy`, `python-dotenv`, `google-generativeai`).
  - [x] Configure environment variables template (`.env.example`) and security ignores (`.gitignore`).
- [x] **Draft Project Proposal (`DOCS/PROJECT_PROPOSAL.md`)**
  - [x] Formulate project purpose and dual core objectives (Ticketing + AI Concierge).
  - [x] Identify primary target audiences (tourists, families, cultural sites).
  - [x] Define the 4 core system modules (User Management, Catalog Directory, Ticketing Engine, AI Concierge).
  - [x] Define task distribution and roles for single-member delivery (Alessio Manera, ID: 905639).
  - [x] Ensure strict 1-page A4 PDF length constraint for Moodle submission.
- [x] **Coding Guidelines & Documentation Standards**
  - [x] Author comprehensive project overview and coding standards (`README.md`).
  - [x] Compile detailed market and competitor analysis report (`DOCS/Competitor_Analysis.md`).
  - [x] Synthesize course guidelines, exam rules, and architectural constraints (`DOCS/Project_Analysis_Report.md`).
- [ ] **Submit 1-Page Proposal to Professor on Moodle**
  - [ ] Generate clean A4 PDF from `DOCS/PROJECT_PROPOSAL.md`.
  - [ ] Submit on Moodle before the semester proposal deadline.
  - [ ] Review professor feedback and integrate any required adjustments.

---

## Phase 2: Design System & Neubrutalism Architecture
- [x] **Adopt Neubrutalism Design Philosophy ([neubrutalism.com](https://neubrutalism.com/))**
  - [x] Choose Neubrutalism / Bauhaus aesthetic to deliver extreme simplicity, high contrast, and zero cognitive load.
  - [x] Disable dark mode to strictly preserve the high-contrast stark white print aesthetic.
- [x] **Define Design Tokens & CSS Custom Properties (`static/css/variables.css`)**
  - [x] Color palette: Pure White base (`#FFFFFF`), Solid Black border/text (`#000000`), Bauhaus Red (`#FF3333`), Bauhaus Blue (`#0055FF`), Bauhaus Yellow (`#FFCC00`).
  - [x] Border tokens: Aggressive `3px solid #000000`.
  - [x] Shadow tokens: Hard offset block shadows (`4px 4px 0px 0px #000000`).
  - [x] Border radius: Strictly `0px` across all containers, inputs, buttons, and cards.
  - [x] Spacing & sizing scales: Modular rem-based units for consistent whitespace.
- [x] **Typography & Micro-interactions Setup**
  - [x] Import and configure `Inter` sans-serif font family with heavy weights (800/900) for headings.
  - [x] Configure progressive text wrapping: `text-wrap: balance` on headings, `text-wrap: pretty` on paragraphs.
  - [x] Implement tactile mechanical button click states (`transform: translate(4px, 4px)` with shadow collapse on `:active`).
- [x] **Core Layout & Component Styles**
  - [x] Build master grid and flexbox layout utilities (`static/css/layout.css`).
  - [x] Style UI components: Neubrutalist cards, badges, inputs, alerts, navigation bars (`static/css/components.css`).
  - [x] Create helper classes and utilities (`static/css/utilities.css`).
  - [x] Build main CSS aggregator (`static/css/style.css`).
- [x] **Accessibility & Performance Standards**
  - [x] Ensure WCAG AAA contrast ratio across all text and interactive elements.
  - [x] Set explicit dimensions / aspect-ratios on images to guarantee zero Cumulative Layout Shift (CLS).

---

## Phase 3: Frontend Templates & Client-Side Scripts (Static / Jinja2)
- [x] **Base Layout Template (`templates/base.html`)**
  - [x] Establish HTML5 semantic structure (`<header>`, `<nav>`, `<main>`, `<footer>`).
  - [x] Implement dynamic navigation bar with conditional Auth states (Login/Register vs. Profile/Logout).
  - [x] Set up flash messaging block with dismissible Neubrutalist alert boxes.
- [x] **Core Page Templates**
  - [x] `templates/index.html`: Landing page with hero banner, feature breakdown, and call-to-action buttons.
  - [x] `templates/museums.html`: Grid catalog displaying cultural venues with location, description, and action buttons.
  - [x] `templates/booking.html`: Ticket selection interface with exhibition pickers, date selections, and checkout card.
  - [x] `templates/guide.html`: Interactive AI Cultural Concierge chat interface with message stream and prompt suggestions.
  - [x] `templates/login.html`: Neubrutalist login form with email/password validation.
  - [x] `templates/register.html`: Registration form with cultural preference tagging selector.
- [x] **Client-Side Interactions (`static/js/main.js`)**
  - [x] Form submission handlers and client-side validation helpers.
  - [x] Toast notification and asynchronous response feedback.
  - [x] Responsive mobile menu toggle handler.

---

## Phase 4: Backend Setup & SQLite Database Schema
- [x] **Flask Application Factory Architecture (`app.py`)**
  - [x] Implement `create_app()` factory pattern for clean lifecycle management.
  - [x] Configure SQLite URI (`sqlite:///app.db`) and secret keys via `python-dotenv`.
  - [x] Register Blueprints (`main_bp` in `routes.py`, `auth_bp` in `auth.py`).
  - [x] Auto-create database tables on startup within app context.
- [x] **Relational Database Schema Definition (`models.py`)**
  - [x] `User` model: `id`, `name`, `email` (unique), `password_hash`, `preferences`, one-to-many relationship with `Ticket`.
  - [x] `Museum` model: `id`, `name`, `description`, `location`, `image_url`, one-to-many relationship with `Exhibition`.
  - [x] `Exhibition` model: `id`, `museum_id` (foreign key), `title`, `start_date`, `end_date`, relationship with `Ticket`.
  - [x] `Ticket` model: `id`, `user_id` (foreign key), `exhibition_id` (foreign key), `booking_date`, `status`.
- [x] **Database Seeding (`seed.py`)**
  - [x] Populate SQLite database with authentic Italian cultural venues (e.g., Uffizi Gallery, Colosseum Archaeological Park, Doge's Palace, Museo Egizio).
  - [x] Populate corresponding exhibitions and dates.

---

## Phase 5: Dynamic Integration & Authentication
- [x] **User Authentication & Session Management (`auth.py`)**
  - [x] Registration handler (`/register` POST) with secure password hashing via `werkzeug.security.generate_password_hash`.
  - [x] Login handler (`/login` POST) with password verification via `check_password_hash`.
  - [x] Session establishment (`session['user_id']`) and logout handler (`/logout`) that clears session state.
  - [x] Route protection via `@login_required` decorator for authenticated views (`/booking`, `/guide`).
- [x] **Dynamic Catalog & Booking Workflows (`routes.py`)**
  - [x] Query and inject dynamic `Museum` records into `museums.html`.
  - [x] Query dynamic `Exhibition` records into `booking.html` with support for URL query preselection (`?museum_id=X`).
  - [x] Asynchronous booking endpoint (`POST /api/book`): validate user session, create `Ticket` record in SQLite, and return JSON status.

---

## Phase 6: AI Cultural Concierge & Grounded RAG Feature
- [x] **Gemini API Integration & Grounding Workflow**
  - [x] Configure Google Generative AI SDK (`google-generativeai`) with secure `GEMINI_API_KEY`.
  - [x] Implement lightweight RAG (Retrieval-Augmented Generation): query SQLite `Museum` and `Exhibition` tables and inject fresh catalog context into the Gemini system prompt.
  - [x] Restrict AI responses strictly to grounded database facts to eliminate hallucinations.
- [x] **Conversational Interface & Session Memory (`routes.py`, `templates/guide.html`)**
  - [x] Implement chat API endpoint (`POST /api/chat`) with session-based rolling history window (capped to prevent cookie size overflow).
  - [x] Build asynchronous chat UI with animated typing indicators, instant message appending, and error fallbacks.
  - [x] Dynamically personalize recommendations based on stored user `preferences`.

---

## Phase 7: Quality Assurance, Security, & Testing
- [ ] **Code Quality & Modularity Audit (6 Points Academic Evaluation)**
  - [ ] Verify adherence to DRY principles across Python blueprints, Jinja2 templates, and CSS stylesheets.
  - [ ] Add comprehensive docstrings and inline comments across all functions and route handlers.
  - [ ] Ensure consistent code formatting and PEP 8 compliance for backend Python files.
- [ ] **Security & Error Handling Verification**
  - [ ] Verify SQL injection protection via SQLAlchemy parameterized queries.
  - [ ] Verify Cross-Site Scripting (XSS) prevention via Jinja2 auto-escaping.
  - [ ] Verify secure password storage (Werkzeug SHA-256 / PBKDF2).
  - [ ] Implement custom HTTP error pages (`404.html`, `500.html`).
- [ ] **Cross-Device & Responsive Usability Testing**
  - [ ] Validate responsive layout on desktop, tablet, and mobile viewports.
  - [ ] Verify keyboard navigation and screen-reader accessibility.
  - [ ] Verify zero visual regressions or layout shifts during dynamic interactions.

---

## Phase 8: Final Packaging, Documentation & Exam Presentation
- [ ] **Project Setup & Run Documentation**
  - [ ] Finalize `README.md` with complete, step-by-step instructions for running the project locally.
  - [ ] Verify virtual environment activation commands for Windows (`powershell`), macOS, and Linux.
  - [ ] Ensure all dependencies are locked in `requirements.txt`.
- [ ] **Oral Exam Presentation Preparation (6 Points Academic Evaluation)**
  - [ ] Structure presentation outline emphasizing project purpose, technical architecture, strengths, and limitations.
  - [ ] Prepare live demonstration walkthrough (User Registration -> Museum Browsing -> AI Concierge Recommendation -> Ticket Booking).
  - [ ] Document potential future enhancements (e.g., QR-code digital ticket generation, calendar sync).
- [ ] **Moodle Submission Packaging**
  - [ ] Clean temporary files, caches (`__pycache__`, `.pytest_cache`), and non-essential folders prior to bundling.
  - [ ] Package final archive (`.zip`) containing the source code, SQLite database seed, and documentation document as requested in the project guide.
  - [ ] Submit on Moodle ahead of the deadline.
