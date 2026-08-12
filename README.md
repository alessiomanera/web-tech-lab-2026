# Museum Ticketing & AI Guide

**Author:** Alessio Manera  
**Student ID:** 905639  
**Course:** Lab of Web Technologies (AY 2025-26)  

## Project Description
A web application for booking museum and cultural site tickets, integrated with AI-powered guidance and personalized recommendations. Its main functionalities include streamlining ticket purchasing and providing tailored cultural suggestions.

## Technology Stack
- **Frontend:** HTML, Vanilla CSS, Vanilla JavaScript
- **Backend:** Python with Flask
- **Database/Storage:** (To be defined, e.g., SQLite)

## Project Guidelines & Coding Best Practices

As a core requirement for this project, the following best practices MUST be adhered to throughout development. We are building a premium application, not a monolithic script.

### 1. Clean & Reusable Code
- **DRY Principle (Don't Repeat Yourself):** Extract common logic into reusable functions or modules.
- **Modularity:** Avoid monolithic files. 
  - Break down HTML into reusable templates using Flask/Jinja2 (`{% extends %}`, `{% include %}`).
  - Split CSS into logical files (e.g., `variables.css`, `layout.css`, `components.css`).
  - Keep JavaScript focused on specific features (e.g., `api.js`, `ui.js`).
- **Meaningful Naming:** Use descriptive variables and function names. A function name should describe exactly what it does.

### 2. File Organization
Keep the project structured logically:
- `/templates/` for all HTML views.
- `/static/css/` for stylesheets.
- `/static/js/` for client-side scripts.
- `/static/images/` for assets.
- `app.py` for backend routing, keeping complex logic in separate Python modules (e.g. `/models`, `/utils`) if it grows.

### 3. Frontend Aesthetics & UI/UX
- **Design System (70/20/10 Blend):**
  - 70% Modern Editorial (Lots of whitespace, elegant typography, refined borders).
  - 20% Contemporary Digital (Clean structural components, subtle border-radii).
  - 10% Neo-Brutalist Interaction (Physical, snappy hover states, 3px active state translation).
- **Custom 4-Color Palette:**
  - Base: Soft Linen (`#F1EBDD`)
  - Dark: Carbon Black (`#171717`)
  - Primary Accent: Primary Scarlet (`#D62F24`)
  - Secondary Accent: Steel Azure (`#174A8B`)
- **Vanilla CSS:** Use a custom design system with CSS Variables for consistent colors and spacing.
- **Responsiveness:** Ensure mobile-first or at least fully responsive design using Flexbox/Grid.
- **Micro-interactions:** Add subtle hover effects, transitions, and modern design principles to make the UI feel premium and alive.

### 4. Version Control
- Commit often with descriptive messages.
- Use branches for new features if experimenting.

### 5. Comments & Documentation
- Document complex backend algorithms, especially the AI recommendation logic.
- Add comments to HTML/CSS where the structure isn't immediately obvious.

## Running the Project
1. Install Python 3.
2. Create a virtual environment: `python -m venv venv`
3. Activate the environment: 
   - Windows: `.\venv\Scripts\activate`
   - Mac/Linux: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `python app.py`
