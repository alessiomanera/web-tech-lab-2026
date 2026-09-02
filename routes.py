"""
routes.py
---------
Main routing blueprint for the Museum & Cultural Experience platform.
Handles page rendering for Home, Explore Experiences, Museums, 4-Step Booking Wizard,
the AI Cultural Concierge, User Profile Dashboard, and asynchronous REST APIs.
Uses raw sqlite3 with parameterized queries for all database access.
"""
import os
import random
import string
import json
import sqlite3
import logging
from datetime import datetime, timezone
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, abort
from auth import login_required
from database import get_db

main_bp = Blueprint('main', __name__)

# Single source of truth for bookable time slots — validated here, and the
# only place `booking()` reads them from before handing them to the template.
VALID_TIME_SLOTS = ['09:30 - 11:00', '11:30 - 13:00', '14:30 - 16:00', '16:30 - 18:00']


def generate_booking_code():
    """Generates a memorable booking reference code, e.g. EXP-2026-A91F7Q."""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=6))
    return f"EXP-2026-{suffix}"


def _parse_json_column(value, default=None):
    """Safely parses a JSON text column, returning the default on failure."""
    if default is None:
        default = []
    if not value:
        return default
    try:
        return json.loads(value)
    except (json.JSONDecodeError, TypeError):
        return default


def _safe_int(value):
    """Returns int(value), or None if value is missing, empty, or non-numeric."""
    try:
        return int(value)
    except (TypeError, ValueError):
        return None


def _current_user(db):
    """
    Returns the logged-in user's row, or None if the id in the session no
    longer exists. Only reached from @login_required views, so session
    ['user_id'] is always set by the time this runs.
    """
    return db.execute(
        "SELECT * FROM users WHERE id = ?", (session['user_id'],)
    ).fetchone()


def _lookup_experience_by_id(db, raw_id):
    """Resolves a raw (possibly missing/non-numeric) experience id to a dict, or None."""
    exp_id = _safe_int(raw_id)
    if exp_id is None:
        return None
    row = db.execute("SELECT * FROM experiences WHERE id = ?", (exp_id,)).fetchone()
    return _exp_row_to_dict(row) if row else None


def _lookup_experience_by_museum(db, raw_museum_id):
    """Resolves a raw museum id to its first bookable experience, or None."""
    museum_id = _safe_int(raw_museum_id)
    if museum_id is None:
        return None
    row = db.execute(
        "SELECT * FROM experiences WHERE museum_id = ? LIMIT 1", (museum_id,)
    ).fetchone()
    return _exp_row_to_dict(row) if row else None


def create_booking(db, user_id, exp_id, visit_date_str, time_slot, guests_count=1, selected_addons=None):
    """
    Validates booking parameters and inserts a new Ticket record in SQLite.
    Returns (ticket_dict, None) on success, or (None, error_message) on failure.
    """
    # Server-side validation
    if not exp_id or not visit_date_str or not time_slot:
        return None, 'Please select an experience, visit date, and time slot.'

    try:
        guests_count = int(guests_count)
        if guests_count < 1 or guests_count > 6:
            return None, 'Guest count must be between 1 and 6.'
    except (ValueError, TypeError):
        return None, 'Invalid guest count.'

    exp = _lookup_experience_by_id(db, exp_id)
    if exp is None:
        return None, 'Selected experience not found.'

    try:
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
        if visit_date < datetime.now().date():
            return None, 'Visit date cannot be in the past.'
    except (ValueError, TypeError):
        return None, 'Invalid date format. Expected YYYY-MM-DD.'

    if time_slot not in VALID_TIME_SLOTS:
        return None, 'Invalid time slot selected.'

    # Handle selected_addons if passed as JSON string or list
    if isinstance(selected_addons, str):
        try:
            requested_addons = json.loads(selected_addons)
        except (json.JSONDecodeError, TypeError):
            requested_addons = []
    elif isinstance(selected_addons, list):
        requested_addons = selected_addons
    else:
        requested_addons = []

    # Never price a booking from the client's numbers. The request only gets to
    # say WHICH add-ons it wants; the name and price are re-read from this
    # experience's own catalog entry. Unknown ids are dropped, and duplicates
    # are collapsed, so a crafted payload cannot invent an add-on or discount.
    catalog_addons = {
        addon['id']: addon for addon in exp['available_addons']
        if isinstance(addon, dict) and 'id' in addon
    }
    addons_list = []
    for requested in requested_addons:
        if not isinstance(requested, dict):
            continue
        addon = catalog_addons.get(requested.get('id'))
        if addon is not None and addon not in addons_list:
            addons_list.append(addon)

    # Calculate total price from the catalog values only
    base_total = exp['base_price'] * guests_count
    addons_total = sum(float(a.get('price', 0)) for a in addons_list) * guests_count
    total_price = base_total + addons_total

    addons_json_str = json.dumps(addons_list)

    # booking_code is UNIQUE; retry on the rare collision instead of 500-ing.
    booking_code = None
    for _ in range(5):
        candidate = generate_booking_code()
        try:
            db.execute(
                """INSERT INTO tickets
                   (booking_code, user_id, experience_id, visit_date, time_slot,
                    guests_count, selected_addons_json, total_price, status)
                   VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                (candidate, user_id, exp['id'], visit_date_str,
                 time_slot, guests_count, addons_json_str,
                 total_price, 'Confirmed')
            )
            db.commit()
            booking_code = candidate
            break
        except sqlite3.IntegrityError:
            continue

    if booking_code is None:
        return None, 'Could not generate a unique booking code. Please try again.'

    # Fetch the inserted ticket for return
    ticket_row = db.execute(
        """SELECT t.*, e.title AS experience_title, e.city AS experience_city
           FROM tickets t
           JOIN experiences e ON t.experience_id = e.id
           WHERE t.booking_code = ?""", (booking_code,)
    ).fetchone()

    return dict(ticket_row), None


# -----------------------------------------------------------------------------
# 1. Page Navigation Routes
# -----------------------------------------------------------------------------

@main_bp.route('/')
def home():
    """
    Renders the main cultural portal landing page.
    Displays hero section, 3-step value workflow, and top featured experiences.
    """
    db = get_db()
    featured = db.execute(
        "SELECT * FROM experiences WHERE is_featured = 1 LIMIT 4"
    ).fetchall()

    if not featured:
        featured = db.execute("SELECT * FROM experiences LIMIT 4").fetchall()

    # Wrap rows so templates can access JSON-parsed properties
    featured_list = [_exp_row_to_dict(row) for row in featured]
    return render_template('index.html', featured=featured_list)


@main_bp.route('/experiences')
def experiences():
    """
    Renders the full 12-Experience catalog.
    Supports filtering by city, theme, and search keyword.
    """
    city_filter = request.args.get('city')
    theme_filter = request.args.get('theme')
    search_query = request.args.get('q')

    db = get_db()

    query = "SELECT * FROM experiences WHERE 1=1"
    params = []

    if city_filter and city_filter.lower() != 'all':
        query += " AND city LIKE ?"
        params.append(f"%{city_filter}%")

    if theme_filter and theme_filter.lower() != 'all':
        query += " AND theme LIKE ?"
        params.append(f"%{theme_filter}%")

    if search_query:
        query += " AND (title LIKE ? OR city LIKE ? OR description LIKE ?)"
        params.extend([f"%{search_query}%"] * 3)

    rows = db.execute(query, params).fetchall()
    all_experiences = [_exp_row_to_dict(row) for row in rows]

    # Get distinct cities for filter pills
    distinct_cities = [r['city'] for r in db.execute("SELECT DISTINCT city FROM experiences ORDER BY city").fetchall()]
    cities = ['All'] + distinct_cities

    return render_template(
        'experiences.html',
        experiences=all_experiences,
        cities=cities,
        selected_city=city_filter or 'All',
        search_query=search_query or ''
    )


@main_bp.route('/experiences/<int:exp_id>')
def experience_detail(exp_id):
    """
    Renders a detailed page for a single cultural experience.
    """
    db = get_db()
    row = db.execute(
        "SELECT * FROM experiences WHERE id = ?", (exp_id,)
    ).fetchone()

    if row is None:
        abort(404)

    exp = _exp_row_to_dict(row)
    return render_template('experience_detail.html', exp=exp)


@main_bp.route('/museums')
def museums():
    """
    Renders the museum catalog page.
    Queries the museums table and passes results to the template.
    """
    db = get_db()
    rows = db.execute("SELECT * FROM museums").fetchall()
    museums_list = [dict(row) for row in rows]
    return render_template('museums.html', museums=museums_list)


@main_bp.route('/booking', methods=['GET', 'POST'])
@login_required
def booking():
    """
    Renders the 4-step Frictionless Booking Wizard.
    Pre-selects experience if passed via ?exp_id=X.
    Also handles POST submissions for the booking form.
    """
    db = get_db()

    rows = db.execute("SELECT * FROM experiences").fetchall()
    all_experiences = [_exp_row_to_dict(row) for row in rows]

    user = _current_user(db)

    selected_exp = None
    ticket = None
    error = None

    if request.method == 'POST':
        exp_id = request.form.get('experience_id')
        visit_date_str = request.form.get('visit_date')
        time_slot = request.form.get('time_slot')
        guests_count = request.form.get('guests_count', 1)
        selected_addons_json = request.form.get('selected_addons_json', '[]')

        if exp_id:
            selected_exp = _lookup_experience_by_id(db, exp_id)

        ticket, error = create_booking(
            db=db,
            user_id=session['user_id'],
            exp_id=exp_id,
            visit_date_str=visit_date_str,
            time_slot=time_slot,
            guests_count=guests_count,
            selected_addons=selected_addons_json
        )
    else:
        preselected_id = request.args.get('exp_id')
        preselected_museum_id = request.args.get('museum_id')
        if preselected_id:
            selected_exp = _lookup_experience_by_id(db, preselected_id)
        elif preselected_museum_id:
            selected_exp = _lookup_experience_by_museum(db, preselected_museum_id)

    return render_template(
        'booking.html',
        experiences=all_experiences,
        selected_exp=selected_exp,
        user=user,
        ticket=ticket,
        error=error,
        time_slots=VALID_TIME_SLOTS
    )


@main_bp.route('/concierge')
@login_required
def concierge():
    """
    Renders the AI Cultural Concierge interactive chat interface.
    Loads the user's live Markdown Cultural Taste Profile from SQLite.
    """
    db = get_db()
    user = _current_user(db)

    taste_items = _parse_taste_profile(user['preferences'] if user else '')

    return render_template('guide.html', user=user, taste_items=taste_items)


# Backward compatibility route
@main_bp.route('/guide')
def guide_redirect():
    return redirect(url_for('main.concierge'))


def _parse_taste_profile(raw_text):
    """
    Parses a Markdown Cultural Taste Profile into structured items
    for clean, aligned template rendering.
    """
    if not raw_text:
        return []
    items = []
    for line in raw_text.splitlines():
        line = line.strip()
        if not line or line.startswith('#'):
            continue
        if line.startswith('-'):
            line = line.lstrip('- ').strip()
        if '**' in line:
            parts = line.split('**')
            if len(parts) >= 3:
                key = parts[1].rstrip(':').strip()
                val = parts[2].lstrip(':').strip()
                items.append({'label': key, 'value': val})
                continue
        items.append({'label': None, 'value': line})
    return items


@main_bp.route('/profile')
@login_required
def profile():
    """
    Renders the user account dashboard with active digital passes,
    past visit history, review submission forms, and the live Cultural Taste Profile.
    """
    db = get_db()
    user = _current_user(db)

    bookings = db.execute(
        """SELECT t.*, e.title AS experience_title, e.city AS experience_city,
                  e.image_url AS experience_image_url, e.base_price,
                  e.duration_minutes, e.available_addons_json
           FROM tickets t
           JOIN experiences e ON t.experience_id = e.id
           WHERE t.user_id = ?
           ORDER BY t.booking_date DESC""",
        (session['user_id'],)
    ).fetchall()

    bookings_list = []
    for row in bookings:
        d = dict(row)
        d['selected_addons'] = _parse_json_column(d.get('selected_addons_json'))
        bookings_list.append(d)

    taste_items = _parse_taste_profile(user['preferences'] if user else '')

    return render_template(
        'profile.html',
        user=user,
        bookings=bookings_list,
        taste_items=taste_items
    )


# -----------------------------------------------------------------------------
# Error Page Preview Routes (for direct verification & testing)
# -----------------------------------------------------------------------------

@main_bp.route('/400')
def preview_400():
    """Renders the custom 400 Bad Request error page."""
    return render_template('400.html'), 400


@main_bp.route('/404')
def preview_404():
    """Renders the custom 404 Not Found error page."""
    return render_template('404.html'), 404


@main_bp.route('/500')
def preview_500():
    """Renders the custom 500 Internal Server Error page."""
    return render_template('500.html'), 500


# -----------------------------------------------------------------------------
# 2. REST API Endpoints
# -----------------------------------------------------------------------------

@main_bp.route('/api/book', methods=['POST'])
@login_required
def api_book():
    """
    API endpoint for confirming a cultural booking.
    Receives experience_id, visit_date, time_slot, guests_count, and selected_addons.
    Calculates total price, inserts a Ticket row in SQLite, and returns confirmation.
    """
    data = request.get_json() or {}
    exp_id = data.get('experience_id')
    visit_date_str = data.get('visit_date')
    time_slot = data.get('time_slot')
    guests_count = data.get('guests_count', 1)
    selected_addons = data.get('selected_addons', [])

    db = get_db()
    ticket, error = create_booking(
        db=db,
        user_id=session['user_id'],
        exp_id=exp_id,
        visit_date_str=visit_date_str,
        time_slot=time_slot,
        guests_count=guests_count,
        selected_addons=selected_addons
    )

    if error:
        status_code = 404 if error == 'Selected experience not found.' else 400
        return jsonify({'error': error}), status_code

    return jsonify({
        'success': True,
        'message': 'Experience booked successfully!',
        'booking_code': ticket['booking_code'],
        'total_price': f"€{ticket['total_price']:.2f}",
        'experience_title': ticket['experience_title'],
        'city': ticket['experience_city'],
        'visit_date': ticket['visit_date'],
        'time_slot': ticket['time_slot']
    })


@main_bp.route('/api/feedback', methods=['POST'])
@login_required
def api_feedback():
    """
    Submits rating and review feedback for a booking.
    """
    data = request.get_json() or {}
    booking_id = data.get('booking_id')
    rating = data.get('rating')
    comment = data.get('comment', '')

    if not booking_id or rating is None:
        return jsonify({'error': 'Missing booking ID or rating.'}), 400

    try:
        rating_value = int(rating)
    except (TypeError, ValueError):
        return jsonify({'error': 'Rating must be a whole number between 1 and 5.'}), 400

    if rating_value < 1 or rating_value > 5:
        return jsonify({'error': 'Rating must be between 1 and 5 stars.'}), 400

    db = get_db()
    ticket = db.execute(
        "SELECT * FROM tickets WHERE id = ? AND user_id = ?",
        (booking_id, session['user_id'])
    ).fetchone()

    if not ticket:
        return jsonify({'error': 'Booking not found.'}), 404

    db.execute(
        """UPDATE tickets
           SET feedback_rating = ?, feedback_text = ?, feedback_date = ?
           WHERE id = ? AND user_id = ?""",
        (rating_value, comment, datetime.now(timezone.utc).isoformat(),
         booking_id, session['user_id'])
    )
    db.commit()

    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})


# NOTE: Grounding Scope Limitation
# The AI Concierge grounds exclusively on the `experiences` table (the 12 curated bookable packages).
# It does NOT ground on the `museums` or `exhibitions` tables, nor does it maintain live venue
# logistics (e.g., general opening hours, street addresses, or physical museum accessibility).
# It is designed specifically to match visitor preferences to curated experience packages.
def _call_gemini_concierge(user_message, current_profile, all_experiences, api_key):
    """
    Calls Google Gemini API with Grounded RAG context from the SQLite experiences catalog.
    Extracts response text and updated Markdown taste profile.
    """
    import google.generativeai as genai
    genai.configure(api_key=api_key)

    # Format the 12 catalog experiences for grounding
    catalog_summary = []
    for exp in all_experiences:
        catalog_summary.append(
            f"- ID: {exp['id']} | Title: \"{exp['title']}\" | City: {exp['city']} | "
            f"Theme: {exp['theme']} | Duration: {exp['duration_minutes']} mins | "
            f"Base Price: €{exp['base_price']:.2f} | Highlights: {exp.get('highlights', '')}"
        )
    catalog_text = "\n".join(catalog_summary)

    system_instruction = f"""You are the official AI Cultural Concierge for Italy Experience, an elite cultural booking platform in Italy.
You help visitors discover the right museum and cultural experiences in Italy based on their interests, party size, pacing, and tastes.

GROUNDED CATALOG (Only recommend from these verified experiences):
{catalog_text}

USER'S CURRENT TASTE PROFILE:
{current_profile or "No profile established yet (new user)."}

CRITICAL INSTRUCTIONS:
1. Speak in a warm, knowledgeable, culturally refined Italian concierge voice (fluent in English, using tasteful Italian greetings like Benvenuto, Ciao, Perfetto).
2. When you recommend any specific package from the catalog, you MUST include this exact booking trigger tag in your response:
   [RECOMMEND: id=<ID>, title="<TITLE>", city="<CITY>", price=<PRICE>]
   For example: [RECOMMEND: id=1, title="Uffizi VIP Masterpieces Tour", city="Florence", price=65.00]
3. Keep recommendations concise, vivid, and helpful (2-3 short paragraphs max).
   Use plain prose. For emphasis use **bold** or *italic* only — no headings,
   bullet lists, tables, or code blocks; the chat renders only those two.
4. At the very end of your response, if the user revealed new tastes, preferences, group details, or favorite cities, provide an updated Markdown Taste Profile starting exactly with the delimiter:
---TASTE_PROFILE---
### Cultural Taste Profile
- **Primary Interests:** <interests>
- **Visit Pacing:** <pacing>
- **Group Style:** <style>
- **Preferred Perks:** <perks>
- **Favorite Cities:** <cities>
"""

    # "-latest" aliases track Google's current release, so a pinned id cannot
    # go stale underneath us the way gemini-2.5-flash did. Both fallbacks are
    # verified reachable; the list is de-duplicated so an explicit GEMINI_MODEL
    # equal to one of them is not retried twice.
    model_name = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
    candidate_models = [model_name, "gemini-flash-lite-latest", "gemini-3.6-flash"]
    candidate_models = list(dict.fromkeys(candidate_models))

    last_error = None
    for m in candidate_models:
        try:
            model = genai.GenerativeModel(
                model_name=m,
                system_instruction=system_instruction
            )
            response = model.generate_content(user_message)
            if response and response.text:
                full_text = response.text
                updated_profile = None
                if "---TASTE_PROFILE---" in full_text:
                    parts = full_text.split("---TASTE_PROFILE---")
                    response_text = parts[0].strip()
                    updated_profile = parts[1].strip()
                else:
                    response_text = full_text.strip()
                return response_text, updated_profile
        except Exception as e:
            last_error = e
            continue

    raise last_error or Exception("Unable to generate response from Gemini API.")


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    AI Cultural Concierge endpoint.
    Performs grounded RAG querying the SQLite catalog of 12 experiences
    plus the user's current Markdown taste profile using Google Gemini.
    """
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Please enter a message.'}), 400

    db = get_db()
    user = _current_user(db)

    all_exp_rows = db.execute("SELECT * FROM experiences").fetchall()
    all_experiences = [_exp_row_to_dict(row) for row in all_exp_rows]

    api_key = os.environ.get("GEMINI_API_KEY")

    # If Gemini API key is configured, execute real Gemini RAG
    if api_key and api_key != "your_gemini_api_key_here":
        try:
            response_text, updated_profile = _call_gemini_concierge(
                user_message=user_message,
                current_profile=user['preferences'] if user else None,
                all_experiences=all_experiences,
                api_key=api_key
            )
            if updated_profile:
                db.execute(
                    "UPDATE users SET preferences = ? WHERE id = ?",
                    (updated_profile, session['user_id'])
                )
                db.commit()
            return jsonify({
                'response': response_text,
                'updated_profile': updated_profile or (user['preferences'] if user else None),
                'offline': False
            })
        except Exception as err:
            # Grounded RAG is best-effort: on any API failure (no network,
            # bad key, quota) we degrade to the local heuristic matcher below
            # rather than failing the user's request.
            logging.warning("Gemini Concierge unavailable, using local fallback: %s", err)

    # Heuristic fallback if API key is not present or failed
    matched_exp = None
    for exp in all_experiences:
        if (exp['city'].lower() in user_message.lower() or
                exp['theme'].lower() in user_message.lower()):
            matched_exp = exp
            break
    if not matched_exp and all_experiences:
        matched_exp = all_experiences[0]

    if matched_exp:
        ai_response_text = (
            f"Benvenuto! Based on your interest, I highly recommend exploring "
            f"**{matched_exp['title']}** in {matched_exp['city']}.\n\n"
            f"It offers a {matched_exp['duration_minutes']}-minute curated journey "
            f"covering {matched_exp['highlights']}.\n\n"
            f"[RECOMMEND: id={matched_exp['id']}, title=\"{matched_exp['title']}\", "
            f"city=\"{matched_exp['city']}\", price={matched_exp['base_price']:.2f}]\n\n"
            f"Would you like me to customize this with an expert docent or audio guide?"
        )
    else:
        ai_response_text = (
            "Benvenuto! I'm your AI Cultural Concierge. Tell me what kind of art or history "
            "you love in Italy — try mentioning a city like Florence, Rome, or Venice, or a theme "
            "like Renaissance, Ancient Roman, or Food & Wine."
        )

    # offline=True: this reply came from the deterministic keyword matcher,
    # not Gemini RAG (no key configured, or the API call failed).
    return jsonify({
        'response': ai_response_text,
        'updated_profile': user['preferences'] if user else None,
        'offline': True
    })


@main_bp.route('/api/profile/reset-memory', methods=['POST'])
@login_required
def api_reset_memory():
    """Resets the user's AI Cultural Taste Profile to default."""
    db = get_db()
    db.execute(
        "UPDATE users SET preferences = NULL WHERE id = ?",
        (session['user_id'],)
    )
    db.commit()
    return jsonify({'success': True, 'message': 'Taste profile reset successfully.'})


# -----------------------------------------------------------------------------
# 3. Row-to-Dict Helpers (for JSON column parsing)
# -----------------------------------------------------------------------------

def _exp_row_to_dict(row):
    """
    Converts a sqlite3.Row from the experiences table into a dict
    with parsed JSON columns (included_items, available_addons) for template use.
    """
    d = dict(row)
    d['included_items'] = _parse_json_column(d.get('included_items_json'))
    d['available_addons'] = _parse_json_column(d.get('available_addons_json'))
    return d
