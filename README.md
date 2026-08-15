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

- **Frontend:** HTML5 (semantic markup, Jinja2 template inheritance), Vanilla CSS3 (custom design system), Vanilla JavaScript (ES6+ for asynchronous `fetch` requests and dynamic UI updates).
- **Backend:** Python 3 with the Flask framework (modular Blueprint architecture: `routes.py`, `auth.py`).
- **Database & ORM:** SQLite managed via Flask-SQLAlchemy (`models.py`).
- **AI Engine:** Google Gemini API (`gemini-1.5-flash`) via the `google-generativeai` SDK, implementing Retrieval-Augmented Generation (RAG) over the SQLite catalog.

---

## Design System & UI/UX (Neubrutalism)

The user interface strictly adheres to the **Neubrutalism** design philosophy (inspired by [neubrutalism.com](https://neubrutalism.com/) and Bauhaus minimalism), engineered for extreme visual clarity, simplicity, and zero cognitive friction:

- **High-Contrast Canvas:** Stark white background (`#FFFFFF`) with solid black text and high-contrast `3px` solid black borders (`#000000`).
- **Hard Offset Drop-Shadows:** `4px 4px 0px 0px #000000` with zero blur for distinct depth separation.
- **Zero Border-Radius:** `0px` border-radius across all buttons, cards, modal dialogs, and input fields.
- **Bauhaus Primary Color Accents:**
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
├── models.py              # SQLAlchemy database models (User, Museum, Exhibition, Ticket)
├── routes.py              # Main Blueprint: page routes and API endpoints (/api/book, /api/chat)
├── auth.py                # Authentication Blueprint: registration, login, logout, @login_required
├── seed.py                # Database population script with sample museums and exhibitions
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
│   │   ├── style.css      # Master stylesheet aggregator
│   │   ├── variables.css  # CSS custom properties (colors, borders, shadows, spacing)
│   │   ├── layout.css     # Grid and Flexbox responsive layout containers
│   │   ├── components.css # Neubrutalist UI components (cards, buttons, forms, alerts)
│   │   └── utilities.css  # Utility classes
│   ├── js/
│   │   └── main.js        # Asynchronous form handlers and UI interactions
│   └── images/            # Static image assets
└── templates/
    ├── base.html          # Master Jinja2 layout with navigation and alerts
    ├── index.html         # Hero landing page and feature highlights
    ├── museums.html       # Museum & cultural site catalog grid
    ├── booking.html       # Exhibition ticket selection and reservation interface
    ├── guide.html         # AI Cultural Concierge conversational chat interface
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
