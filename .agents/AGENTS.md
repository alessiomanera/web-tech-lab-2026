# Local Project Rules

> 🌍 **Note**: Global coding standards (Modularity, UX, Docs) are inherited from Global Rules. 
> *Only project-specific architecture, stack quirks, and setup instructions go here.*

## 1. Project Boundaries & Architecture
- **No Monolithic Code:** Do not create massive files. Break logic down into smaller, modular files.
- **Backend (Python/Flask):** Keep `app.py` clean. Route definitions should use Blueprints (e.g., `routes.py`, `auth.py`). Complex logic should go into `/models`, `/utils`, etc.
- **Database:** SQLite via Flask-SQLAlchemy.
- **Frontend Framework:** Vanilla JS, Vanilla CSS, and HTML with Jinja2. Do NOT use frontend frameworks like React, Vue, or CSS frameworks like Tailwind unless explicitly requested.

## 2. Modularity & DRY
- **HTML:** MUST use Jinja2 inheritance (`{% extends 'base.html' %}`, `{% include %}`).
- **CSS:** MUST be split into logical files (`variables.css`, `layout.css`, `components.css`) and imported into a main stylesheet. No inline styles.
- **JavaScript:** Keep scripts modular and focused (e.g., `api.js`, `ui.js`).

## 3. UI/UX & Aesthetics (70/20/10 Blend)
- **Design System:** 
  - 70% Modern Editorial (Lots of whitespace, elegant typography, refined borders, clean and sophisticated layout).
  - 20% Contemporary Digital (Slight modern web polish, clean structural components).
  - 10% Neo-Brutalist Interaction (Physical, snappy hover and active states on buttons and interactive elements).
- **Color Palette (Custom 4-Color):**
  - Base: Soft Linen (`#F1EBDD`)
  - Dark: Carbon Black (`#171717`)
  - Primary Accent: Primary Scarlet (`#D62F24`)
  - Secondary Accent: Steel Azure (`#174A8B`)
- **Theme Toggle:** Must include a Light/Dark mode toggle switch that persists state via `localStorage`.
- **Micro-interactions:** Snappy, neo-brutalist "press" effects.
- **Responsiveness:** Ensure mobile-first or fully responsive design using Flexbox/Grid.

## 4. Git Workflow
> **CRITICAL RULE**: Always stay on the `testing` branch for development. Do NOT commit directly to `main`. When features are ready, they must be merged into `main` via Pull Requests.
