# Oral Exam Presentation & Defense Guide
**Course:** Lab of Web Technologies (AY 2025–26)  
**Project:** Museum Ticketing & AI Cultural Guide (Italy Experience)  
**Author:** Alessio Manera (Student ID: 905639) — **Group:** Group-11 (Single-person group)  
**Evaluator:** Prof. Yucel  

---

## 1. Executive Summary & Problem Framing

### The Problem
Italy houses over 4,000 cultural institutions and millions of annual visitors, yet the digital visit experience remains fragmented:
- Traditional ticketing platforms (TicketOne, Vivaticket) are transactional, cluttered, and offer zero contextual guidance.
- Generic AI chatbots (ChatGPT) hallucinate non-existent exhibition hours, unavailable tickets, or invent inaccurate prices.
- Visitors spend hours bouncing between disparate booking sites, travel blogs, and museum directories.

### The Solution: "Italy Experience"
A unified full-stack cultural experience platform and grounded AI concierge:
1. **Curated Experience Economy:** 12 curated VIP and thematic Italian cultural packages (e.g., Uffizi VIP Masterpieces, Colosseum Twilight Walk) spanning 6 major art cities.
2. **Frictionless 4-Step Booking Engine:** Streamlined reservation flow with real-time add-on calculations (Audio Guides, Art Historian Docents) and instant digital pass generation.
3. **Grounded RAG Cultural Concierge:** An AI concierge powered by Google Gemini, grounded strictly on the SQLite catalog to eliminate hallucinations, render interactive booking cards directly in the chat, and build a persistent user taste memory profile.

---

## 2. System Architecture & Modularity

```
+-----------------------------------------------------------------------------------------+
|                                    PRESENTATION LAYER                                   |
|   - Semantic HTML5 & Jinja2 Template Inheritance (templates/base.html)                  |
|   - Custom Neubrutalist CSS Design System (variables, layout, components, utilities)     |
|   - Modular Vanilla JavaScript (ES6+ async fetch, booking wizard state machine)         |
+-----------------------------------------------------------------------------------------+
                                             |
                                             v  HTTP / REST JSON
+-----------------------------------------------------------------------------------------+
|                                    APPLICATION LAYER                                    |
|   - Python 3 / Flask with Application Factory Pattern (app.py)                          |
|   - Modular Blueprints:                                                                 |
|       * main_bp (routes.py): Catalog, 4-Step Booking, Concierge RAG, Error Handlers     |
|       * auth_bp (auth.py): Registration, Werkzeug Password Hashing, Session Management   |
|   - Route Protection: Custom @login_required Decorator                                  |
+-----------------------------------------------------------------------------------------+
                                             |
                      +----------------------+----------------------+
                      |                                             |
                      v                                             v
+------------------------------------------+  +-------------------------------------------+
|               DATA LAYER                 |  |           EXTERNAL AI ENGINE              |
| - SQLite3 via Python Standard Library    |  | - Google Gemini Generative AI SDK         |
| - Parameterized Queries (?)              |  | - Grounded RAG Catalog Injection          |
| - PRAGMA foreign_keys = ON               |  | - Actionable Tag Parsing ([RECOMMEND:...])|
| - Dynamic Markdown Taste Memory          |  | - Resilient Local Heuristic Fallback      |
+------------------------------------------+  +-------------------------------------------+
```

---

## 3. Five-Minute Live Demonstration Script

| Time | Step & Screen | What to Show & Explain to Professor |
| :--- | :--- | :--- |
| **0:00 - 0:45** | **1. Landing Page (`/`)** | - Showcase **Neubrutalist design system**: stark high contrast (`#FFFFFF`/`#000000`), `3px` solid borders, `4px` drop-shadows, zero border-radius, and mechanical button press transitions (`translate(4px, 4px)`).<br>- Highlight featured cultural experiences and 3-step value workflow. |
| **0:45 - 1:30** | **2. Experience Catalog (`/experiences`)** | - Demonstrate multi-filter querying (filter by city like *Florence*, theme like *Renaissance*, or search keyword like *Botticelli*).<br>- Demonstrate the Standard vs. Compact view switcher with `localStorage` persistence. |
| **1:30 - 2:30** | **3. 4-Step Booking Wizard (`/booking`)** | - Select experience package with dynamic add-ons (Private Art Historian, Audio Guide).<br>- Show real-time price calculations on the client.<br>- Pick date (+90 day bound) and time slot, submit booking.<br>- Present the instant digital confirmation pass with unique reference code (`EXP-2026-XXXX`). |
| **2:30 - 3:45** | **4. Grounded AI Concierge (`/concierge`)** | - Ask a question: *"I am visiting Florence and love Renaissance painting, but have only 2 hours."*<br>- Explain the **RAG Grounding Pipeline**: SQLite experiences catalog injected into system instruction; Gemini matches package and returns vivid advice with an actionable `[RECOMMEND: ...]` booking card.<br>- Show the live **Taste Memory Panel** dynamically updated with extracted user preferences and show the taste reset option. |
| **3:45 - 4:30** | **5. User Dashboard (`/profile`)** | - View confirmed digital passes with add-on details.<br>- Submit a post-visit rating (1-5 stars) and review comment via `/api/feedback`. |
| **4:30 - 5:00** | **6. Code Quality & Test Suite** | - Open terminal and run `python -m unittest discover -s tests -p "test_*.py" -v`.<br>- Showcase **44 passing unit/integration tests** covering Auth, Database foreign keys, Catalog filters, Booking arithmetic, RAG concierge, and Error pages. |

---

## 4. Grading Rubric Defense (30 + 1 Points)

| Rubric Criterion | Max Pts | Project Implementation & Justification |
| :--- | :---: | :--- |
| **Code Quality & Architecture** | **6 Pts** | Clean Flask Application Factory (`create_app`), modular Blueprints (`routes.py`, `auth.py`), strict separation of concerns, zero monolithic files, comprehensive standard library `unittest` suite (44 tests), 100% parameterized SQL queries (`?`), and PEP 8 compliance. |
| **Innovation & Value** | **4 Pts** | Retrieval-Augmented Generation (RAG) grounding Gemini on SQLite catalog data, dynamic in-chat booking card triggers, and persistent Markdown cultural taste memory. |
| **UX/UI & Accessibility** | **4 Pts** | Custom Neubrutalism design system inspired by *neubrutalism.com*, strictly WCAG AA compliant (AAA on primary text and buttons), keyboard navigable, semantic landmarks (`<header>`, `<nav>`, `<main>`, `<footer>`), custom tactile SVG cursors, and zero Cumulative Layout Shift (CLS). |
| **Deployment & Setup** | **3 Pts** | Zero-dependency setup using Python standard library `sqlite3`, clear step-by-step cross-platform run commands (PowerShell/Bash), clean `.env.example`, and isolated virtual environment. |
| **Collaboration & Git Workflow** | **3 Pts** | Single-person group (Group-11). Rigorous Git branch hygiene with dedicated `testing` development branch, conventional commit messages, and clean commit history. |
| **Presentation & Defense** | **6 Pts** | Confident 5-minute live walkthrough, structured defense deck, transparent architectural trade-off explanations, and verified test execution. |
| **Course Knowledge & Mastery** | **4+1 Pts** | Deep understanding of HTTP request lifecycle, session cookie security, PBKDF2 password hashing, SQL injection mitigation without ORMs, Jinja2 context inheritance, and Vanilla JavaScript DOM manipulation. |

---

## 5. Anticipated Professor Q&A Defense

### Q1: Why did you choose raw SQLite3 instead of SQLAlchemy or an ORM?
> **Answer:** Raw `sqlite3` is part of Python's standard library, adhering strictly to the course philosophy of mastering core fundamentals. To ensure enterprise-grade safety, all queries use parameterized placeholders (`?`), completely neutralizing SQL injection vulnerabilities. Connections are managed per-request via Flask's `g` object and closed cleanly during app context teardown. Furthermore, `PRAGMA foreign_keys = ON` is enforced on every connection to maintain relational integrity (such as cascading deletes on tickets).

### Q2: How does the AI Concierge prevent hallucinations?
> **Answer:** We employ Retrieval-Augmented Generation (RAG) grounded directly in our SQLite database. Before prompting Google Gemini, the backend queries the `experiences` table and formats verified package metadata (IDs, titles, durations, base prices, highlights) directly into Gemini's system instruction. The model is constrained to recommend strictly from this verified catalog and format recommendations using structured `[RECOMMEND: ...]` tags, which our frontend parses into interactive booking cards. If external network access is unavailable or the API key is unconfigured, a resilient local heuristic fallback seamlessly matches user keywords to catalog items.

### Q3: How do you handle password security and user sessions?
> **Answer:** Passwords are never stored in plaintext. We utilize Werkzeug's `generate_password_hash` which applies PBKDF2 with SHA-256 and cryptographic salts. During login, `check_password_hash` verifies the credentials in constant time. Authenticated sessions store only the integer `user_id` inside Flask's cryptographically signed session cookie (signed with `SECRET_KEY`). Protected endpoints are guarded by a custom `@login_required` decorator that redirects unauthenticated requests to `/login`.

### Q4: Why did you implement the Neubrutalism design style?
> **Answer:** Neubrutalism provides high visual clarity and legibility. Stark white backgrounds (`#FFFFFF`), solid black borders (`3px solid #000000`), hard offset drop-shadows (`4px 4px 0px 0px #000`), and bold typography (`Inter` with heavy weights) eliminate visual clutter and cognitive load. High-contrast accent colors (red, blue, yellow) are used purposefully for status badges and calls-to-action, achieving WCAG AA compliance throughout and AAA contrast on primary text. Tactile button states physically depress by `translate(4px, 4px)` on click, simulating a mechanical press.

### Q5: How is the 4-step booking wizard structured?
> **Answer:** The booking wizard operates as a client-side state machine in `static/js/bookingWizard.js` with server-side validation in `routes.py`:
> 1. **Step 1:** Select package and customize add-ons (pricing dynamically recalculated via JS).
> 2. **Step 2:** Choose visit date (validated between today and +90 days) and select one of the daily time slots.
> 3. **Step 3:** Review order breakdown (base tickets + add-ons $\times$ guests).
> 4. **Step 4:** Submit booking via `POST /api/book` or form submit, generating a unique booking reference code (`EXP-2026-XXXX`) and rendering the digital pass.
