# Comprehensive Project, Exam, and Technical Reference

> [!NOTE]
> This document provides a complete, unified analysis of the **Museum Ticketing & AI Guide** project. It merges the official course guidelines, exam rules, project architecture, Neubrutalism design principles, and available class resources into a master reference document.

---

## 1. Project & Group Details
- **Course:** Lab of Web Technologies (a.a. 2025–26)
- **Author:** Alessio Manera (Student ID: 905639)
- **Group:** Group-11 (Single-person group confirmed by Professor Yucel)
- **Target Exam Session:** September 2026
- **Project Topic:** Museum Booking and AI Cultural Guide Web Application
- **Core Objectives:** Streamlining cultural site ticket booking and providing grounded AI recommendations.

---

## 2. Exam Structure & Academic Grading Rules

### Grade Breakdown (30+1 Scale)
The course evaluation consists of two complementary components (both graded out of 30+1, minimum 18 points required in each):
1. **Written Exam (50%):** 5 multiple-choice questions + 3 open-ended questions based strictly on the course lecture slides.
2. **Project & Oral Exam (50%):** Technical evaluation and project presentation evaluated across the following areas:
   - **Code Quality (6 points):** Clean, modular, well-commented, comprehensively documented, secure, and aligned with the proposal.
   - **Collaboration & Group Structure (6 points):** Clearly defined roles, knowledge sharing, and domain responsibility.
   - **Project Presentation (6 points):** Clear explanation of project purpose, features, strengths, and limitations.
   - **Knowledge of Course Contents (6 points):** Effective incorporation and mastery of technologies covered in class (HTML, CSS, JS, Flask, SQLite).
   - **Innovation & Creativity (2 points):** Originality of the idea and problem-solving approaches (e.g., RAG AI concierge).
   - **User Experience & Interface Design (2 points):** Usability, accessibility (WCAG), Neubrutalism design quality, and responsiveness.
   - **Deployment & Maintenance (2 points):** Clear run instructions and future architectural maintainability.

### Academic Deadlines Workflow (Countdown to Exam)
- **4 weeks prior to exam:** Submit group member list (`zeynep.yucel@unive.it`). *(Completed: Group-11)*.
- **3 weeks prior to exam:** Submit 1-page proposal draft on Moodle (`DOCS/PROJECT_PROPOSAL.md`).
- **2 weeks prior to exam:** Receive feedback and adjust proposal if required.
- **1 week prior to exam:** Submit final project archive (`.zip`) on Moodle containing source code and documentation.
- **Exam Day:** Brief oral presentation and live application walkthrough.

---

## 3. Architecture & Technical Stack

### Core Technologies
- **Frontend:** HTML5 (semantic Jinja2 templates), Vanilla CSS3 (custom Neubrutalism design tokens), Vanilla JavaScript (ES6+ for asynchronous REST requests).
- **Backend:** Python 3 with the Flask framework (modular Blueprints: `routes.py`, `auth.py`).
- **Database:** SQLite managed via standard library `sqlite3` with parameterized queries (`database.py`, `schema.sql`).
- **External Services:** Google Gemini API (`gemini-3.7-flash`, configurable via `GEMINI_MODEL`) with Grounded RAG over SQLite catalog data.

### Design System: Neubrutalism ([neubrutalism.com](https://neubrutalism.com/))
- **Aesthetic Principles:** High contrast, raw geometry, and zero cognitive friction.
- **Visual Tokens:**
  - Base Background: Pure White (`#FFFFFF`)
  - Borders: Heavy `3px solid #000000`
  - Shadows: Hard offset `4px 4px 0px 0px #000000` (zero blur)
  - Corner Radii: Strictly `0px`
  - Accent Highlights: Purposeful, high-contrast accents for buttons, status badges, and focus indicators
- **Typography:** `Inter` sans-serif with heavy weights (800/900) for titles and progressive text-wrap enhancements.
- **Micro-interactions:** Snappy mechanical button depress (`transform: translate(4px, 4px)`) on click.
- **Theme:** High-contrast Light Mode.

---

## 4. Modular Codebase Architecture

```text
web-tech-lab-2026/
├── app.py                 # Application factory and error handler registration
├── database.py            # SQLite connection context manager & initialization
├── schema.sql             # SQL database definition (users, museums, experiences, tickets)
├── routes.py              # Main routes and API handlers (/booking, /api/chat, /api/feedback)
├── auth.py                # Authentication routes (/register, /login, /logout) and @login_required
├── seed.py                # Database seeding script with Top 12 Curated Italian Experiences
├── requirements.txt       # Dependencies: Flask, python-dotenv, google-generativeai
├── static/                # Modular CSS and client-side JS
│   ├── css/               # variables.css, layout.css, components.css, utilities.css, style.css
│   ├── images/            # Authentic local photos in /experiences/ and /museums/, custom SVG cursors
│   └── js/                # main.js (coordinator), api.js (fetch calls), ui.js (cursors), bookingWizard.js
└── templates/             # Jinja2 templates extending base.html
    ├── base.html          # Global navigation, alerts, and footer
    ├── index.html         # Landing page with 3-step value workflow & trending packages
    ├── experiences.html   # Full 12-Experience catalog with search & city filter pills
    ├── experience_detail.html # Deep-dive view for individual experiences
    ├── booking.html       # 4-step frictionless booking wizard
    ├── guide.html         # AI Concierge conversational chat view with taste memory
    ├── profile.html       # User dashboard: active digital passes, visit review loop, taste profile
    ├── login.html         # Login interface
    └── register.html      # Registration with preference tags
```

---

## 5. Course Documentation & Reference Mapping

Official university materials and course guidelines used to validate technical alignment:
- **`DOCS/AY2025_2026_project_guide.pdf`**: Official requirements, submission rules, and grading breakdown.
- **`DOCS/AY2024_2025_project_outlines.pdf`**: Historical topics and project scope reference.
- **`_CLASS_RESOURCES/` (untracked/local)**: Lecture slides (`all_merged_slides_web_tech_2026.pdf`) and weekly practical lab exercises (`week_2` through `week_5`).
