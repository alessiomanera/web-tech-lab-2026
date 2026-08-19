# Local Project Rules

> 🌍 **Note**: Global coding standards (Modularity, UX, Docs) are inherited from Global Rules. 
> *Only project-specific architecture, stack quirks, and setup instructions go here.*

## 1. Project Boundaries & Architecture
- **No Monolithic Code:** Do not create massive files. Break logic down into smaller, modular files.
- **Backend (Python/Flask):** Keep `app.py` clean. Route definitions should use Blueprints (e.g., `routes.py`, `auth.py`). Complex logic should go into `/models`, `/utils`, etc.
- **Database:** SQLite via raw standard library `sqlite3` (no ORM).
- **Frontend Framework:** Vanilla JS, Vanilla CSS, and HTML with Jinja2. Do NOT use frontend frameworks like React, Vue, or CSS frameworks like Tailwind unless explicitly requested.

## 2. Modularity & DRY
- **HTML:** MUST use Jinja2 inheritance (`{% extends 'base.html' %}`, `{% include %}`).
- **CSS:** MUST be split into logical files (`variables.css`, `layout.css`, `components.css`) and imported into a main stylesheet. No inline styles.
- **JavaScript:** Keep scripts modular and focused (e.g., `api.js`, `ui.js`).

## 3. UI/UX & Aesthetics (Neo-Brutalism)
- **Design System:** 
  - Pure Neo-Brutalism (https://neubrutalism.com/). Stark white backgrounds, aggressive thick black borders (`3px`), hard offset black shadows (`4px 4px 0px 0px #000`), zero border radii (`0px`).
- **Color Palette & Accents:**
  - Base/Background: Pure White (`#FFFFFF`)
  - Border/Text: Solid Black (`#000000`)
  - Deliberate, high-contrast accent highlights (Red `#FF3333`, Blue `#0055FF`, Yellow `#FFCC00`) applied purposefully for actions, badges, and focus indicators.
- **Typography:** Strictly `Inter` (sans-serif) across all elements. Heavy weights (800/900) for headings.
- **Theme Toggle:** NO DARK MODE. Neubrutalism relies on the stark white contrast.
- **Micro-interactions:** Snappy, neo-brutalist "press" effects. Buttons should physically depress (`translate(4px, 4px)`) and lose their shadow on active/hover to simulate a mechanical click.
- **Cursor Discipline:** The pointer cursor (`var(--cursor-pointer)`) must ONLY appear over truly clickable elements (`a[href]`, active `button:not(:disabled)`, form controls). Never on static cards or non-interactive badges.
- **Universal Box-Sizing:** Maintain `*, *::before, *::after { box-sizing: border-box; }` at the root of `layout.css` to prevent horizontal button/card overflow.
- **Responsiveness:** Ensure mobile-first or fully responsive design using Flexbox/Grid.

## 4. Git Workflow
> **CRITICAL RULE**: Always stay on the `testing` branch for development. Do NOT commit directly to `main`. When features are ready, they must be merged into `main` via Pull Requests.
- **Release Protocol:** When creating official tagged releases (e.g. `v1.0.0`), verify that 100% of automated tests pass on `testing`, merge `testing` into `main`, tag the release, push `main` and tags to remote, and immediately switch back to `testing`.

## 5. Repository Cleanliness & Privacy (Professor-Ready Standard)
- **Pristine Codebase:** The entire repository must remain clean, tidy, and presentation-ready at all times for sharing with the professor.
- **No Personal Notes in Git:** Never commit personal comments, rough working notes, private links, or scratch files to Git. All private notes and links MUST reside exclusively in the `_PERSONAL/` folder (which is git-ignored).
- **Untracked Course Resources:** Class exercises, lectures, and bulk reference files must remain in `_CLASS_RESOURCES/` (git-ignored). Only the official PDF references required for project citation (`AY2025_2026_project_guide.pdf`, `AY2024_2025_project_outlines.pdf`) are maintained in `DOCS/`.
- **Public Documentation Boundaries:** `DOCS/` must contain only authoritative public deliverables (`PROJECT_PROPOSAL.md`, `Competitor_Analysis.md`, and official course PDFs). All internal student study notes, countdown schedules, and oral exam defense scripts reside exclusively in `_PERSONAL/` (`Presentation_Guide.md`, `Project_Analysis_Report.md`).
- **Immutable Project Proposal:** `DOCS/PROJECT_PROPOSAL.md` represents the final, immutable proposal submitted to the professor and must remain untouched once finalized.

## 6. Anti-Reinvention & Design System Fidelity
- **Check Existing Components First:** Never reinvent utilities, components, or UI patterns. Always check and build upon existing CSS rules (`variables.css`, `layout.css`, `components.css`, `utilities.css`) and modular JS patterns.
- **Strict Neubrutalism Reference:** Adhere strictly to the design system patterns at https://neubrutalism.com/ (stark high-contrast white `#FFFFFF`, `3px` solid black borders, `4px 4px 0px 0px #000` drop-shadows, zero `0px` border-radius, and mechanical click state transitions).
- **Authorized Tech Stack Only:** Strictly follow the course project guide: HTML5 (Jinja2), Vanilla CSS3, Vanilla JavaScript (ES6+), Python 3 with Flask, SQLite via raw standard library `sqlite3` (no ORM), and Google Gemini API (`google-generativeai`).

## 7. Testing & Quality Assurance Standard
- **Automated Test Suite:** Maintain standard library `unittest` suites under `tests/`. All database tests must run against isolated temporary SQLite instances (using `app.py create_app(test_config=...)`) with `PRAGMA foreign_keys = ON`.
- **Zero SQL Injection & 100% Parameterization:** Every database query must use parameterized placeholders (`?`).
