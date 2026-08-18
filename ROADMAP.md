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
  - [x] Choose Neubrutalism aesthetic to deliver extreme simplicity, high contrast, and zero cognitive load.
  - [x] Disable dark mode to strictly preserve the high-contrast stark white print aesthetic.
- [x] **Define Design Tokens & CSS Custom Properties (`static/css/variables.css`)**
  - [x] Color palette: Pure White base (`#FFFFFF`), Solid Black border/text (`#000000`), High-contrast Red (`#FF3333`), Electric Blue (`#0055FF`), Cyber Yellow (`#FFCC00`).
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

## Phase 3: Frontend Templates & Client-Side Scripts (Experience Economy UI)
- [x] **Base Layout Template (`templates/base.html`)**
  - [x] Establish HTML5 semantic structure (`<header>`, `<nav>`, `<main>`, `<footer>`).
  - [x] User-centric navigation: `Home`, `Explore Experiences`, `Tailor Experience (AI)`, `Book Now`, `My Experiences`.
  - [x] Set up flash messaging block with dismissible Neubrutalist alert boxes.
- [x] **Experience Economy Page Templates**
  - [x] `templates/index.html`: Landing page with hero banner, 3-step value workflow, and trending packages.
  - [x] `templates/experiences.html`: Full 20-Experience catalog with search bar and city/theme filter pills.
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
  - [x] Populate SQLite database with **Top 20 Curated Italian Cultural Experiences** across 9 major cities (Florence, Rome, Venice, Milan, Turin, Naples, Verona, Palermo, Bologna).
  - [x] Seed 10 baseline cultural institutions and sample user account with initialized Markdown Taste Profile.

---

## Phase 5: Dynamic Integration & Authentication
- [x] **User Authentication & Session Management (`auth.py`)**
  - [x] Registration handler (`/register` POST) with secure password hashing via `werkzeug.security.generate_password_hash`.
  - [x] Login handler (`/login` POST) with password verification via `check_password_hash`.
  - [x] Session establishment (`session['user_id']`) and logout handler (`/logout`).
  - [x] Route protection via `@login_required` decorator (`/booking`, `/concierge`, `/profile`).
- [x] **Dynamic Catalog & Booking Workflows (`routes.py`)**
  - [x] Query and render 20 experiences with search and city filter on `/experiences`.
  - [x] 4-step wizard endpoint `/booking` with support for URL preselection (`?exp_id=X` or `?museum_id=Y`).
  - [x] Booking submission handler (`POST /booking`): validate input server-side, compute total with add-ons, insert row in `tickets`, and show a real digital confirmation pass.
  - [x] Feedback submission endpoint (`POST /api/feedback`).

---

## Phase 6: AI Cultural Concierge & Grounded RAG Feature
- [x] **Gemini API Integration & Grounding Workflow**
  - [x] Configure Google Generative AI SDK (`google-generativeai`) with secure `GEMINI_API_KEY`.
  - [x] Ground system prompt directly on the 20 SQLite experiences to eliminate hallucinations.
  - [x] In-chat actionable booking card triggers (`[RECOMMEND: id=X, title="Y", city="Z", price=W]`).
- [x] **Dynamic Markdown Taste Memory Pipeline (`routes.py`, `templates/guide.html`)**
  - [x] Background preference extraction: automatically updates `preferences` column in `users` table as structured Markdown after each conversation.
  - [x] Live Taste Memory side panel in chat view and user dashboard (`/profile`).
  - [x] Option to reset/refine taste memory on demand (`POST /api/profile/reset-memory`).

---

## Phase 7: Quality Assurance, Security, & Testing
- [ ] **Code Quality & Modularity Audit (6 Points Academic Evaluation)**
  - [ ] Verify adherence to DRY principles across Python blueprints, Jinja2 templates, and CSS stylesheets.
  - [ ] Add comprehensive docstrings and inline comments across all functions and route handlers.
  - [ ] Ensure consistent code formatting and PEP 8 compliance for backend Python files.
- [x] **Security & Error Handling Verification**
  - [x] Verify SQL injection protection via raw SQLite3 parameterized queries.
  - [x] Verify Cross-Site Scripting (XSS) prevention via Jinja2 auto-escaping.
  - [x] Verify secure password storage (Werkzeug SHA-256 / PBKDF2).
  - [x] Implement custom HTTP error pages (`400.html`, `404.html`, `500.html`).
- [x] **Cross-Device & Responsive Usability Testing**
  - [x] Validate responsive layout on desktop, tablet, and mobile viewports.
  - [x] Verify keyboard navigation and screen-reader accessibility.
  - [x] Verify zero visual regressions or layout shifts during dynamic interactions.
- [x] **Experience Catalog & Asset Fidelity Audit (1-by-1 Insertion Check)**
  - [x] Individually inspect each of the 20 cultural experience entries in `seed.py` and the SQLite database.
  - [x] Replace any mismatched or generic placeholder imagery with verified, authentic local stock photos across all 10 museums and 20 experiences (`/static/images/museums/` and `/static/images/experiences/`).
  - [x] Cross-check all 20 experiences for accurate city landmarks, durations, transparent pricing, highlight tags, and museum foreign key integrity.

---

## Phase 8: Final Packaging, Documentation & Exam Presentation
- [ ] **Project Setup & Run Documentation**
  - [ ] Finalize `README.md` with complete, step-by-step instructions for running the project locally.
  - [ ] Verify virtual environment activation commands for Windows (`powershell`), macOS, and Linux.
  - [ ] Ensure all dependencies are locked in `requirements.txt`.
- [ ] **Oral Exam Presentation Preparation (6 Points Academic Evaluation)**
  - [ ] Structure presentation outline emphasizing project purpose, technical architecture, strengths, and limitations.
  - [ ] Document potential future enhancements:
    - [ ] **Curated Color Palette Reduction & Light/Dark Theme Architecture:** Simplify the multi-color primary palette (reducing simultaneous red, blue, yellow) down to a strict monochrome base (`#FFFFFF` / `#000000`) with a single refined accent, and implement a high-contrast Neubrutalist Light/Dark theme toggle.
    - [ ] **Digital Pass Enhancements:** Dynamic QR-code ticket rendering and calendar sync integration.
- [ ] **Moodle Submission Packaging**
  - [ ] Clean temporary files, caches (`__pycache__`, `.pytest_cache`), and non-essential folders prior to bundling.
  - [ ] Package final archive (`.zip`) containing the source code, SQLite database seed, and documentation document as requested in the project guide.
  - [ ] Submit on Moodle ahead of the deadline.
