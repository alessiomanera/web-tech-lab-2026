# Project Implementation Roadmap

This document outlines the step-by-step implementation plan for the Museum Ticketing & AI Guide application. It is designed to be updated as the project evolves.

## Phase 1: Foundation & Planning (Current)
- [x] Review project requirements and guidelines.
- [x] Setup repository and define directory skeleton.
- [x] Write project proposal (`PROPOSAL.md`).
- [x] Define coding guidelines and README.
- [ ] Submit 1-page proposal to the professor.

## Phase 2: Design & UI Mockups
- [ ] Define the color palette, typography, and core CSS variables.
- [ ] Create wireframes/mockups for core pages: Home, Museum Listing, Ticket Booking, Profile/Recommendations.
- [ ] Build the base HTML template (`base.html`) with header and footer.

## Phase 3: Frontend Development (Static)
- [ ] Develop `index.html` (Landing page with featured museums).
- [ ] Develop `museums.html` (List/Grid view of all cultural sites).
- [ ] Develop `booking.html` (Ticket selection interface).
- [ ] Implement responsive Vanilla CSS styling.
- [ ] Add basic JS interactions (modals, form validations).

## Phase 4: Backend Setup & Database
- [ ] Initialize Flask application (`app.py`).
- [ ] Define database schema (Users, Museums, Tickets, Preferences).
- [ ] Integrate database with Flask (using SQLAlchemy or raw SQLite).
- [ ] Create basic routes for rendering templates.

## Phase 5: Dynamic Integration
- [ ] Connect frontend forms to Flask endpoints (e.g., submitting a booking).
- [ ] Implement user authentication (Login/Register).
- [ ] Fetch and display museum data dynamically from the database.

## Phase 6: AI Guidance & Recommendations Feature
- [ ] Develop a simple recommendation algorithm based on user preferences.
- [ ] (Optional) Integrate an external LLM API (like OpenAI or Gemini) for generating dynamic cultural insights.
- [ ] Build the "AI Guide" interface on the frontend.

## Phase 7: Polish, Testing, and Submission
- [ ] Code review against guidelines (No monolithic code, DRY, proper comments).
- [ ] Cross-browser and mobile responsive testing.
- [ ] Write final project documentation and run instructions.
- [ ] Create presentation/slides for the oral exam.
- [ ] Submit project zip archive on Moodle.
