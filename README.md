# Museum Ticketing & AI Cultural Guide

**Author:** Alessio Manera  
**Student ID:** 905639  
**Course:** Lab of Web Technologies (AY 2025–26)  
**Group:** Group-11 (Single-person group)

---

## Project Overview

A full-stack web application designed for discovering and booking tickets to museums and cultural heritage sites, integrated with an AI-powered cultural concierge. The platform combines a streamlined e-ticketing workflow with an intelligent conversational assistant powered by Google Gemini, offering personalized visit recommendations grounded directly in the site's SQLite database.

---

## Technical Stack & Architecture

- **Frontend:** HTML5 (semantic markup, Jinja2 template inheritance), Vanilla CSS3 (custom design system loaded directly), Vanilla JavaScript (ES6+ for asynchronous `fetch` requests and dynamic UI updates).
- **Backend:** Python 3 with the Flask framework (modular Blueprint architecture: `routes.py`, `auth.py`).
- **Database & Storage:** Raw SQLite3 using parameterized queries (Python standard library `sqlite3`), no ORM helper libraries (`database.py`, `schema.sql`).
- **AI Engine:** Google Gemini API (`gemini-3.7-flash`, configurable via `GEMINI_MODEL`) via the `google-generativeai` SDK, implementing Retrieval-Augmented Generation (RAG) over the SQLite catalog.

---

## Design System & UI/UX (Neubrutalism)

The user interface strictly adheres to the **Neubrutalism** design philosophy (inspired by [neubrutalism.com](https://neubrutalism.com/)), engineered for extreme visual clarity, simplicity, and zero cognitive friction:

- **High-Contrast Canvas:** Stark white background (`#FFFFFF`) with solid black text and high-contrast `3px` solid black borders (`#000000`).
- **Hard Offset Drop-Shadows:** `4px 4px 0px 0px #000000` with zero blur for distinct depth separation.
- **Zero Border-Radius:** `0px` border-radius across all buttons, cards, modal dialogs, and input fields.
- **Vibrant Primary & Accent Colors:**
  - Primary Red: `#FF3333`
  - Primary Blue: `#0055FF`
  - Primary Yellow: `#FFCC00`
- **Typography:** Strictly `Inter` (sans-serif) across all elements, with heavy font weights (800/900) for section headings and balanced typographic text-wrapping.
- **Tactile Micro-interactions:** Mechanical button press effect (`transform: translate(4px, 4px)` with shadow collapse on click/active).
- **Theme:** Strictly Light Mode to preserve stark contrast and print aesthetic.
- **Accessibility:** Strict WCAG AAA contrast compliance and zero Cumulative Layout Shift (CLS).

---

## Project Structure

```text
web-tech-lab-2026/
├── app.py                 # Application factory and entry point
├── database.py            # SQLite connection context manager & initialization
├── schema.sql             # SQL database definition (tables for users, museums, experiences, tickets, etc.)
├── routes.py              # Main Blueprint: page routes and API endpoints (/booking, /api/chat, /api/feedback)
├── auth.py                # Authentication Blueprint: registration, login, logout, @login_required
├── seed.py                # Database population script with Top 20 Curated Italian Cultural Experiences
├── requirements.txt       # Python package dependencies
├── .env.example           # Template for environment variables (GEMINI_API_KEY, FLASK_SECRET_KEY)
├── DOCS/
│   ├── PROJECT_PROPOSAL.md # 1-page A4 project proposal for academic submission
│   ├── AY2025_2026_project_guide.pdf # Official course & project guidelines
│   ├── AY2024_2025_project_outlines.pdf # Historical project topics reference
│   ├── Competitor_Analysis.md # Comprehensive European/Italian market research & UX audit
│   └── Project_Analysis_Report.md # Course guidelines and technical reference
├── static/
│   ├── css/
│   │   ├── style.css      # Master stylesheet aggregator (retained for fallback)
│   │   ├── variables.css  # CSS custom properties (colors, borders, shadows, spacing, cursors)
│   │   ├── layout.css     # Grid and Flexbox responsive layout containers & custom cursors
│   │   ├── components.css # Neubrutalist UI components (cards, buttons, forms, alerts, wizard)
│   │   └── utilities.css  # Utility classes
│   ├── js/
│   │   ├── main.js        # Global JavaScript coordinator
│   │   ├── api.js         # API integration helpers (chat, feedback, reset taste profile)
│   │   ├── ui.js          # Cursor injection and tactile UI state actions
│   │   └── bookingWizard.js # 4-step wizard state machine and dynamic addon price calculations
│   └── images/            # Static image assets & custom SVG cursors (cursor.svg, cursor-pointer.svg)
└── templates/
    ├── base.html          # Master Jinja2 layout with navigation and alerts
    ├── index.html         # Landing page with 3-step value workflow & trending packages
    ├── experiences.html   # Full 20-Experience catalog with search & city filter pills
    ├── experience_detail.html # Deep-dive view for individual experiences
    ├── booking.html       # 4-step frictionless booking wizard
    ├── guide.html         # AI Cultural Concierge conversational chat view with taste memory
    ├── profile.html       # User dashboard: active digital passes, visit review loop, taste profile
    ├── login.html         # User login form
    └── register.html      # User registration form with cultural preferences selector
```

---

## Installation & Setup Instructions

### Prerequisites
- Python 3.10+ installed on your system.
- Git.

### Setup Steps
1. **Clone the repository:**
   ```bash
   git clone https://github.com/alessiomanera/web-tech-lab-2026.git
   cd web-tech-lab-2026
   ```

2. **Create and activate a virtual environment:**
   - **Windows (PowerShell):**
     ```powershell
     python -m venv venv
     .\venv\Scripts\Activate.ps1
     ```
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

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables:**
   - Copy `.env.example` to `.env`:
     ```bash
     cp .env.example .env
     ```
   - Set your `GEMINI_API_KEY` and optional `FLASK_SECRET_KEY` in `.env`.

5. **Seed the database (Optional but recommended):**
   ```bash
   python seed.py
   ```

6. **Run the application:**
   ```bash
   python app.py
   ```
   Open your browser and navigate to `http://127.0.0.1:5000/`.
