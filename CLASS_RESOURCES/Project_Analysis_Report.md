# Comprehensive Project, Exam, and Resources Reference

> [!NOTE]
> This document provides a complete, unified analysis of the Museum Ticketing & AI Guide project. It merges the official course guidelines, exam rules, project structure analysis, and available class resources into a single master reference document for AI assistants (like Claude) to understand the project's context, constraints, and architecture.

## 1. Project & Group Details
- **Course:** Lab of Web Technologies (a.a. 2025-26)
- **Author:** Alessio Manera
- **Group:** Group-11 (Single-person group confirmed by Professor Yucel)
- **Target Session:** September 2026
- **Project Topic:** Museum Booking and Info Web App
- **Goal:** A web application for booking tickets to cultural sites, augmented with an AI-powered cultural recommendation system.
- **Core Functionalities:** Streamlining ticket purchasing and providing tailored cultural suggestions.

## 2. Exam Structure & General Rules
- **Grade Breakdown:** The exam is 50% written and 50% project/oral. Both are graded out of 30+1 points, and a minimum of 18 points in each is required to pass.
- **Prerequisite:** You absolutely cannot take the written or oral exam without first passing "Introduction to Coding and Data Management".
- **Written Exam Format:** Based strictly on the course slides, consisting of exactly 5 multiple-choice questions and 3 open-ended questions (as per the professor's email). A sample exam is available on Moodle for practice.
- **Academic Year Limit:** Both the written and oral exams must be passed within the same academic year. Because September is the last session of the academic year, failing or missing one part means you will lose any retained grades and must redo both parts the following year.

### Timelines & Required Steps
*(Deadlines count backwards from the official September exam date once it is announced).*
- **4 weeks before the exam:** Submit group members. *(Completed: Registered as Group-11)*.
- **3 weeks before the exam:** Submit the 1-page project proposal (initial draft) on Moodle.
- **2 weeks before the exam:** Receive feedback from the professor. If revisions are requested, the proposal must be revised and resubmitted.
- **1 week before the exam:** Submit the final project archive (.zip, .tar.gz) on Moodle. It must include a document with the project's description, run instructions, and role contributions. Submissions after the deadline will not be considered.
- **Exam Day (Oral Presentation):** Deliver a brief presentation discussing the web application, emphasizing its purpose, features, strengths, and potential limitations.

---

## 3. Architecture & Project Requirements

### Technical Stack & Constraints
- **Required Technologies:** HTML (structure and content), CSS (presentation), JavaScript (dynamic behavior), and Python with the Flask framework (web server management).
- **Architecture Requirement:** The project must contain several static and dynamic web pages, managed by a web server capable of handling different kinds of HTTP requests.
- **Frontend:** HTML5 (Jinja2 templates), Vanilla CSS (custom design system, no Tailwind), Vanilla JavaScript.
- **Backend:** Python 3 with Flask.
- **Database:** SQLite via Flask-SQLAlchemy.

### Source Code Organization
The project follows a standard, modular Flask application structure:
```text
Web_Tech_Lab_2026/
├── app.py                 # Application factory and entry point
├── models.py              # SQLAlchemy database models
├── routes.py              # Flask blueprints and route definitions
├── requirements.txt       # Python dependencies
├── static/                # Static assets
│   ├── css/               # Vanilla CSS files (to be organized by layout/components)
│   ├── js/                # Client-side JavaScript
│   └── images/            # Image assets
└── templates/             # HTML templates (Jinja2)
    ├── base.html          # Master layout template
    ├── index.html         # Landing page
    ├── museums.html       # Museum listing view
    └── booking.html       # Ticket booking interface
```

### Core Modules Analysis
- **`app.py`**: Implements the Application Factory pattern (`create_app()`). Configures the SQLite database (`app.db`), initializes SQLAlchemy, registers the `main_bp` blueprint, and automatically creates tables. 
- **`models.py`**: Defines the relational database schema (`User`, `Museum`, `Exhibition`, `Ticket`). The `User` model includes a `preferences` field (JSON/text) for the AI recommendation engine.
- **`routes.py`**: Utilizes Flask Blueprints to manage routing cleanly (`/`, `/museums`, `/booking`, `/guide`).

### Design & Coding Constraints
> [!IMPORTANT]
> The `README.md` strictly enforces specific best practices:
> - **No Monolithic Code**: Extract logic into reusable functions/modules. CSS must be split logically (variables, layout, components). HTML must use Jinja2 inheritance.
> - **Aesthetics**: Build a premium application using a custom design system, modern typography, responsive Flexbox/Grid, and micro-interactions.
> - **AI Integration**: The backend will handle an AI recommendation algorithm based on the `preferences` column in the `User` model, potentially leveraging an external LLM API.

---

## 4. Class Resources Analysis
The `CLASS_RESOURCES` directory contains official course materials, lecture slides, and weekly practical exercises to guide the development process.

### Course Documents & Guidelines
- **`AY2025_2026_project_guide.pdf`**: The most relevant guide for the current academic year (2025-2026). Contains formatting, submission, and grading criteria.
- **`all_merged_slides_web_tech_2026.pdf`**: A comprehensive, 11MB file containing all lecture slides. This is the primary reference for the written exam and technical approaches taught in class.
- **`AY2024_2025_project_outlines.pdf`**: Previous year's project outlines, for historical context.

### Weekly Exercises & Solutions
The folder contains a structured progression of lab exercises corresponding to the course syllabus:
- **`week_2_HTML_exercise/` & `week_2_HTML_exercise_solution/`**: Foundational HTML structure.
- **`week_3_css_exercise_solution/`**: Styling exercises (Vanilla CSS).
- **`week_4_flask_examples/` & `week_4_js_execise_solution/`**: Backend development with Flask and client-side interactions with JavaScript.
- **`week_5_database_exercise/`**: Examples covering database integration using Flask and databases.

> [!TIP]
> When implementing specific features (e.g., database models, Flask routing, CSS layouts), refer back to these `week_X` folders to ensure the code style aligns with what the professor has taught.

---

## 5. Current Status & Next Steps
According to `ROADMAP.md`, Phase 1 (Foundation) is complete. 

**Immediate Next Steps (Phase 2 & 3):**
1. Define the color palette and core CSS variables in `/static/css/`.
2. Build out the frontend HTML structure in `/templates/` using the established `base.html` layout.
3. Implement responsive Vanilla CSS styling and basic JS interactions before moving on to connecting dynamic forms to the Flask backend (Phase 5).
