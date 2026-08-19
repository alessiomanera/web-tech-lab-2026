# Project Proposal: Museum Ticketing & AI Cultural Guide

**Course:** Lab of Web Technologies (AY 2025–26) | **Author:** Alessio Manera (ID: 905639) | **Group:** Group-11 (single-person group) | **Date:** August 19, 2026

---

### 1. Purpose of the Project
The proposed project is a full-stack web application designed to modernize the cultural visit experience in Italy. It serves a dual mission: providing a streamlined, friction-free ticket booking platform for museums and curated cultural experiences, while acting as an intelligent, context-aware AI cultural concierge. By integrating generative AI grounded directly in the application's relational database, the system dynamically personalizes cultural recommendations and assists users in planning tailored visit itineraries.

### 2. Target Users
- **Tourists & Cultural Visitors:** rapid, intuitive ticket reservations and personalized exhibition and museum discovery across major Italian art cities.
- **Families & Time-Constrained Visitors:** customized suggestions adapted to visit duration, group composition, or audience age.
- **Museums & Cultural Sites:** a lightweight, modern web platform for experience showcases, visitor engagement, and inventory management.

### 3. System Modules
- **Module 1: User Authentication & Cultural Profiling:** secure registration and login (Flask session management, Werkzeug password hashing), account dashboard, and dynamic cultural taste memory tracking.
- **Module 2: Experience & Museum Catalog Directory:** dynamic catalog presenting curated Italian cultural experiences and baseline museums, detailing venues, themes, durations, pricing, and highlights, with real-time relational querying.
- **Module 3: A 4-Step Ticketing & Reservation Engine:** frictionless booking wizard featuring package selection, customizable add-ons, visit date and time-slot selection, instant digital booking confirmation, and post-visit rating/feedback.
- **Module 4: Grounded AI Cultural Concierge:** conversational discovery powered by the Google Gemini API, using Retrieval-Augmented Generation grounded in SQLite catalog data to minimize hallucinations, trigger actionable in-chat booking cards, and refine user taste profiles over time.

### 4. Tools & Technical Stack
- **Frontend:** HTML5 (semantic structure, Jinja2 template inheritance), Vanilla CSS3 (custom Neubrutalist design system, no build tools or CSS frameworks), Vanilla JavaScript (ES6+ for async fetch calls, DOM updates, booking wizard state).
- **Backend:** Python 3 with Flask (modular Blueprint architecture: `routes.py`, `auth.py`).
- **Database:** SQLite via the standard library `sqlite3` module, using parameterized queries for SQL-injection protection (`database.py`, `schema.sql`).
- **External AI Integration:** Google Gemini API via the official `google-generativeai` SDK, with a configurable model endpoint and a resilient local fallback.

### 5. UI/UX Design Paradigm (Neubrutalism)
The interface follows the Neubrutalism aesthetic (inspired by [neubrutalism.com](https://neubrutalism.com/)) for extreme visual clarity, high readability, and zero cognitive load: a stark high-contrast layout (solid black borders, hard offset drop-shadows, no border radius), deliberate accent-color highlighting for calls-to-action and status indicators, and tactile micro-interactions such as mechanical button-press feedback, built to WCAG AA contrast standards, with AAA-level contrast on primary text.

### 6. Task Distribution & Roles
Single-person project (Alessio Manera) with end-to-end full-stack ownership:
- **Database & Architecture:** relational schema design, entity relationships, SQLite initialization, sample dataset seeding (`seed.py`).
- **Backend Development:** RESTful endpoints (`/api/book`, `/api/chat`, `/api/feedback`), blueprint routing, authentication logic, Gemini API integration.
- **Frontend & UI/UX Design:** semantic Jinja2 templates, Neubrutalism CSS design system, responsive Flexbox/Grid layouts, client-side async scripts.
- **Quality Assurance & Documentation:** route testing, WCAG accessibility verification, run documentation, oral exam presentation.
