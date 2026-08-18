# Project Proposal: Museum Ticketing & AI Cultural Guide
**Course:** Lab of Web Technologies (AY 2025–26)  
**Author:** Alessio Manera (ID: 905639) — **Group:** Group-11 (Single-person group)

---

### 1. Purpose of the Project
The proposed project is a full-stack web application designed to modernize the cultural visit experience. It serves a dual mission: providing a streamlined, friction-free ticket booking platform for museums and exhibitions, while acting as an intelligent, context-aware AI cultural concierge. By integrating generative AI grounded in the site's database, the application dynamically personalizes cultural recommendations and assists users in planning tailored visit itineraries.

### 2. Target Users
- **Tourists & Cultural Visitors:** Seeking rapid, intuitive ticket reservations and personalized exhibition discovery.
- **Families & Time-Constrained Visitors:** Requiring customized suggestions adapted to specific visit durations, group composition, or audience age.
- **Museums & Cultural Sites:** Seeking a lightweight, modern web platform for exhibition showcases, visitor engagement, and ticket inventory management.

### 3. System Modules
- **Module 1 — User Authentication & Cultural Profiling:** Secure registration and login (using Flask session management and password hashing), user profile management, and cultural interest tagging.
- **Module 2 — Museum & Exhibition Catalog Directory:** Dynamic catalog presenting cultural venues, active/upcoming exhibitions, opening hours, and location details, with real-time relational querying.
- **Module 3 — Ticketing & Reservation Engine:** Exhibition slot selection, live ticket availability tracking, booking confirmation generation, and purchase history tracking.
- **Module 4 — AI Cultural Concierge & Recommendation System:** Conversational discovery interface powered by the Google Gemini API, utilizing Retrieval-Augmented Generation (RAG) grounded strictly in SQLite catalog data to prevent hallucinations and generate personalized visit plans.

### 4. Tools & Technical Stack
- **Frontend:** HTML5 (semantic structure, Jinja2 inheritance), Vanilla CSS3 (custom design system), Vanilla JavaScript (ES6+ for asynchronous `fetch` calls and dynamic DOM updates).
- **Backend:** Python 3 with the Flask framework (modular architecture with Blueprints: `routes.py`, `auth.py`).
- **Database:** SQLite managed via Flask-SQLAlchemy ORM (`models.py`).
- **External AI Integration:** Google Gemini API (`gemini-1.5-flash`) via the official `google-generativeai` SDK.

### 5. UI/UX Design Paradigm (Neubrutalism)
The interface is designed around the **Neubrutalism** aesthetic (inspired by [neubrutalism.com](https://neubrutalism.com/)) to deliver extreme visual simplicity and zero cognitive load:
- **High-Contrast Light Theme:** Stark white background (`#FFFFFF`), solid high-contrast black borders (`3px solid #000000`), hard offset drop-shadows (`4px 4px 0px 0px #000000`), zero border radii (`0px`), and vibrant primary/accent colors (`#FF3333`, `#0055FF`, `#FFCC00`).
- **Tactile Micro-interactions:** Mechanical button click responses (`translate(4px, 4px)` with shadow collapse on click) and strict WCAG AAA contrast for maximum accessibility.

### 6. Task Distribution & Roles
*Single-person project (Alessio Manera)* with end-to-end full-stack ownership:
- **Database & Architecture:** Relational schema design, entity relationships, SQLite initialization, and sample dataset seeding (`seed.py`).
- **Backend Development:** RESTful API endpoints (`/api/book`, `/api/chat`), blueprint routing, authentication logic, and Gemini API integration.
- **Frontend & UI/UX Design:** Semantic Jinja2 templates, Neubrutalism CSS design system, responsive Flexbox/Grid layouts, and client-side asynchronous scripts.
- **Quality Assurance & Documentation:** Route testing, WCAG compliance verification, run documentation, and oral exam presentation.
