# Project Implementation Roadmap

This document outlines the step-by-step implementation plan for the Museum Ticketing & AI Guide application. It is designed to be updated as the project evolves.

## Phase 1: Foundation & Planning (Current)
- [x] Review project requirements and guidelines.
- [x] Setup repository and define directory skeleton.
- [x] Write project proposal (`PROPOSAL.md`).
- [x] Define coding guidelines and README.
- [ ] Submit 1-page proposal to the professor.

## Phase 2: Design & UI Mockups
- [x] Define the color palette, typography, and core CSS variables.
- [x] Create wireframes/mockups for core pages: Home, Museum Listing, Ticket Booking, Profile/Recommendations.
- [x] Build the base HTML template (`base.html`) with header and footer.
- [x] Ensure strict WCAG text contrast and design zero-cognitive-load checkout flows.

## Phase 3: Frontend Development (Static)
- [x] Develop `index.html` (Landing page with featured museums).
- [x] Develop `museums.html` (List/Grid view of all cultural sites).
- [x] Develop `booking.html` (Ticket selection interface).
- [x] Implement responsive Vanilla CSS styling.
- [x] Add basic JS interactions (modals, form validations).
- [x] Implement semantic HTML for screen readers and zero CLS image rendering via aspect-ratio.

## Phase 4: Backend Setup & Database
- [x] Initialize Flask application (`app.py`).
- [x] Define database schema (Users, Museums, Tickets, Preferences).
- [x] Integrate database with Flask (using SQLAlchemy or raw SQLite).
- [x] Create basic routes for rendering templates.

## Phase 5: Dynamic Integration
- [x] Connect frontend forms to Flask endpoints (e.g., submitting a booking).
- [x] Implement user authentication (Login/Register).
- [x] Fetch and display museum data dynamically from the database.
- [x] Implement asynchronous, polite error handling for robust booking flows.

## Phase 6: AI Guidance & Recommendations Feature (Gemini API)
- [x] Integrate the `google-genai` Python SDK and secure API keys via `.env`.
- [x] Implement a lightweight RAG (Retrieval-Augmented Generation) flow by fetching SQLite data (museums/exhibitions) and injecting it into the Gemini system prompt to prevent hallucinations.
- [x] Build the "Cultural Concierge" chat interface on the frontend (`/guide`) allowing natural language conversational discovery.
- [x] Dynamically tailor museum descriptions on the site based on the user's `preferences` profile.

## Phase 7: Polish, Testing, and Submission
- [ ] Code review against guidelines (No monolithic code, DRY, proper comments).
- [ ] Cross-browser and mobile responsive testing.
- [ ] Write final project documentation and run instructions.
- [ ] Create presentation/slides for the oral exam.
- [ ] Remove extra reference folders (e.g., `CLASS_RESOURCES`) and non-essential files prior to final submission.
- [ ] Submit project zip archive on Moodle.

## Phase 8: Future Design Refinement
- [ ] Rethink the 70/20/10 Modern Editorial/Contemporary/Neo-Brutalism aesthetic blend.
- [ ] Refine the custom 4-color palette to better suit the project vision if the current palette is unsatisfactory.
