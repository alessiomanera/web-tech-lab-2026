# Project Proposal: Museum Ticketing & AI Cultural Guide

**Course:** Lab of Web Technologies (AY 2025–26)\
**Author:** Alessio Manera (ID: 905639) — **Group:** Group-11 (Single-person group)

---

### 1. Purpose of the Project

The proposed project is a full-stack web application designed to modernize the cultural visit experience in Italy. It serves a dual mission: providing a streamlined, friction-free ticket booking platform for museums and curated cultural experiences, while acting as an intelligent, context-aware AI cultural concierge. By integrating generative AI grounded directly in the application's relational database, the system dynamically personalizes cultural recommendations and assists users in planning tailored visit itineraries.

### 2. Target Users

- **Tourists & Cultural Visitors:** Seeking rapid, intuitive ticket reservations and personalized exhibition and museum discovery across major Italian art cities.
- **Families & Time-Constrained Visitors:** Requiring customized suggestions adapted to specific visit durations, group composition, or audience age.
- **Museums & Cultural Sites:** Seeking a lightweight, modern web platform for experience showcases, visitor engagement, and inventory management.

### 3. System Modules

- **Module 1 — User Authentication & Cultural Profiling:** Secure user registration and login (using Flask session management and Werkzeug password hashing), account dashboard, and dynamic cultural taste memory tracking.
- **Module 2 — Experience & Museum Catalog Directory:** Dynamic catalog presenting 12 curated Italian cultural experiences and baseline museums, detailing venues, themes, durations, pricing, and highlights with real-time relational querying.
- **Module 3 — 4-Step Ticketing & Reservation Engine:** Frictionless booking wizard featuring package selection, customizable add-ons (Audio Guides, Docents, VIP Fast-Track), dedicated visit date and time-slot selection, instant digital pass generation, and post-visit rating/feedback submissions.
- **Module 4 — Grounded AI Cultural Concierge:** Conversational discovery interface powered by the Google Gemini API, utilizing Retrieval-Augmented Generation (RAG) grounded strictly in SQLite catalog data to eliminate hallucinations, trigger actionable in-chat booking cards, and continuously refine user taste profiles.

### 4. Tools & Technical Stack

- **Frontend:** HTML5 (semantic structure, Jinja2 template inheritance), Vanilla CSS3 (custom Neubrutalist design system loaded directly without build tools or external CSS frameworks), Vanilla JavaScript (ES6+ for asynchronous `fetch` calls, dynamic DOM updates, and booking wizard state management).
- **Backend:** Python 3 with the Flask framework (modular architecture with Blueprints: `routes.py`, `auth.py`).
- **Database:** SQLite managed via raw standard library `sqlite3` using parameterized queries for full SQL injection protection and performance (`database.py`, `schema.sql`).
- **External AI Integration:** Google Gemini API via the official `google-generativeai` SDK (grounded on SQLite catalog data, with configurable model endpoint and resilient local fallback).

### 5. UI/UX Design Paradigm (Neubrutalism)

The interface is built around the **Neubrutalism** aesthetic (inspired by [neubrutalism.com](https://neubrutalism.com/)) to deliver extreme visual clarity, high readability, and zero cognitive load:

- **High-Contrast Layout Foundation:** Stark white backgrounds (`#FFFFFF`), solid high-contrast black borders (`3px solid #000000`), hard offset drop-shadows (`4px 4px 0px 0px #000000`), and zero border radii (`0px`).
- **Deliberate Accent Highlights:** Purposeful, high-contrast accent highlights applied strategically to call-to-action buttons, status badges, and interactive indicators while maintaining strict WCAG AA/AAA contrast ratios.
- **Tactile Micro-interactions:** Mechanical button press feedback (`translate(4px, 4px)` with shadow collapse on click/active states) and visible focus indicators for frictionless accessibility.

### 6. Task Distribution & Roles

*Single-person project (Alessio Manera)* with end-to-end full-stack ownership:

- **Database & Architecture:** Relational schema design, entity relationships, raw SQLite3 initialization, and sample dataset seeding (`seed.py`).
- **Backend Development:** RESTful API endpoints (`/api/book`, `/api/chat`, `/api/feedback`), blueprint routing, authentication logic, and Gemini API integration.
- **Frontend & UI/UX Design:** Semantic Jinja2 templates, Neubrutalism CSS design system, responsive Flexbox/Grid layouts, and client-side asynchronous scripts.
- **Quality Assurance & Documentation:** Route testing, WCAG accessibility compliance verification, comprehensive run documentation, and oral exam presentation.
