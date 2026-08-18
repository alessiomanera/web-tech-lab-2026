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
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from auth import login_required
from database import get_db

# TODO: Re-enable Gemini API integration once an API key is configured.
# import google.generativeai as genai

main_bp = Blueprint('main', __name__)


def generate_booking_code():
    """Generates a memorable unique booking reference code, e.g., EXP-2026-A91F."""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=4))
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
    Renders the full 20-Experience catalog.
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
    cities = ['All', 'Florence', 'Rome', 'Venice', 'Milan', 'Turin',
              'Naples', 'Verona', 'Palermo', 'Bologna']

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
        return "Experience not found", 404

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

    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (session['user_id'],)
    ).fetchone()

    selected_exp = None
    ticket = None
    error = None

    if request.method == 'POST':
        exp_id = request.form.get('experience_id')
        visit_date_str = request.form.get('visit_date')
        time_slot = request.form.get('time_slot')
        guests_count = request.form.get('guests_count', 1)
        selected_addons_json = request.form.get('selected_addons_json', '[]')

        # Server-side validation
        if not exp_id or not visit_date_str or not time_slot:
            error = 'Please select an experience, visit date, and time slot.'
        else:
            try:
                guests_count = int(guests_count)
                if guests_count < 1 or guests_count > 6:
                    error = 'Guest count must be between 1 and 6.'
            except (ValueError, TypeError):
                error = 'Invalid guest count.'

            if not error:
                exp_row = db.execute(
                    "SELECT * FROM experiences WHERE id = ?", (exp_id,)
                ).fetchone()
                if not exp_row:
                    error = 'Selected experience not found.'
                else:
                    exp = _exp_row_to_dict(exp_row)
                    selected_exp = exp
                    try:
                        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
                        if visit_date < datetime.now().date():
                            error = 'Visit date cannot be in the past.'
                    except ValueError:
                        error = 'Invalid date format. Expected YYYY-MM-DD.'

                    valid_slots = ['09:30 - 11:00', '11:30 - 13:00', '14:30 - 16:00', '16:30 - 18:00']
                    if time_slot not in valid_slots:
                        error = 'Invalid time slot selected.'

            if not error:
                # Calculate total price
                try:
                    selected_addons = json.loads(selected_addons_json)
                except Exception:
                    selected_addons = []
                base_total = exp['base_price'] * guests_count
                addons_total = sum(float(a.get('price', 0)) for a in selected_addons) * guests_count
                total_price = base_total + addons_total

                booking_code = generate_booking_code()

                db.execute(
                    """INSERT INTO tickets
                       (booking_code, user_id, experience_id, visit_date, time_slot,
                        guests_count, selected_addons_json, total_price, status)
                       VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
                    (booking_code, session['user_id'], exp['id'], visit_date_str,
                     time_slot, guests_count, selected_addons_json,
                     total_price, 'Confirmed')
                )
                db.commit()

                # Fetch the inserted ticket for the success view
                ticket_row = db.execute(
                    """SELECT t.*, e.title AS experience_title, e.city AS experience_city
                       FROM tickets t
                       JOIN experiences e ON t.experience_id = e.id
                       WHERE t.booking_code = ?""", (booking_code,)
                ).fetchone()
                ticket = dict(ticket_row)
    else:
        preselected_id = request.args.get('exp_id')
        preselected_museum_id = request.args.get('museum_id')
        if preselected_id:
            try:
                sel_row = db.execute(
                    "SELECT * FROM experiences WHERE id = ?", (int(preselected_id),)
                ).fetchone()
                if sel_row:
                    selected_exp = _exp_row_to_dict(sel_row)
            except (ValueError, TypeError):
                selected_exp = None
        elif preselected_museum_id:
            try:
                sel_row = db.execute(
                    "SELECT * FROM experiences WHERE museum_id = ? LIMIT 1", (int(preselected_museum_id),)
                ).fetchone()
                if sel_row:
                    selected_exp = _exp_row_to_dict(sel_row)
            except (ValueError, TypeError):
                selected_exp = None

    return render_template(
        'booking.html',
        experiences=all_experiences,
        selected_exp=selected_exp,
        user=user,
        ticket=ticket,
        error=error
    )


@main_bp.route('/concierge')
@login_required
def concierge():
    """
    Renders the AI Cultural Concierge interactive chat interface.
    Loads the user's live Markdown Cultural Taste Profile from SQLite.
    """
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (session['user_id'],)
    ).fetchone()

    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template('guide.html', user=user)


# Backward compatibility route
@main_bp.route('/guide')
def guide_redirect():
    return redirect(url_for('main.concierge'))


@main_bp.route('/profile')
@login_required
def profile():
    """
    Renders the user account dashboard with active digital passes,
    past visit history, review submission forms, and the live Cultural Taste Profile.
    """
    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (session['user_id'],)
    ).fetchone()

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
    return render_template('profile.html', user=user, bookings=bookings_list)


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

    # Server-side validation
    if not exp_id or not visit_date_str or not time_slot:
        return jsonify({'error': 'Please select an experience, visit date, and time slot.'}), 400

    try:
        guests_count = int(guests_count)
        if guests_count < 1 or guests_count > 6:
            return jsonify({'error': 'Guest count must be between 1 and 6.'}), 400
    except (ValueError, TypeError):
        return jsonify({'error': 'Invalid guest count.'}), 400

    db = get_db()
    exp = db.execute(
        "SELECT * FROM experiences WHERE id = ?", (exp_id,)
    ).fetchone()

    if not exp:
        return jsonify({'error': 'Selected experience not found.'}), 404

    try:
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Expected YYYY-MM-DD.'}), 400

    # Validate date is not in the past
    if visit_date < datetime.now().date():
        return jsonify({'error': 'Visit date cannot be in the past.'}), 400

    # Validate time slot
    valid_slots = ['09:30 - 11:00', '11:30 - 13:00', '14:30 - 16:00', '16:30 - 18:00']
    if time_slot not in valid_slots:
        return jsonify({'error': 'Invalid time slot selected.'}), 400

    # Calculate total price
    base_total = exp['base_price'] * guests_count
    addons_total = sum(float(a.get('price', 0)) for a in selected_addons) * guests_count
    total_price = base_total + addons_total

    booking_code = generate_booking_code()

    db.execute(
        """INSERT INTO tickets
           (booking_code, user_id, experience_id, visit_date, time_slot,
            guests_count, selected_addons_json, total_price, status)
           VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
        (booking_code, session['user_id'], exp['id'], visit_date_str,
         time_slot, guests_count, json.dumps(selected_addons),
         total_price, 'Confirmed')
    )
    db.commit()

    return jsonify({
        'success': True,
        'message': 'Experience booked successfully!',
        'booking_code': booking_code,
        'total_price': f"€{total_price:.2f}",
        'experience_title': exp['title'],
        'city': exp['city'],
        'visit_date': visit_date_str,
        'time_slot': time_slot
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

    if not booking_id or not rating:
        return jsonify({'error': 'Missing booking ID or rating.'}), 400

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
        (int(rating), comment, datetime.utcnow().isoformat(),
         booking_id, session['user_id'])
    )
    db.commit()

    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    AI Cultural Concierge endpoint.
    Performs grounded RAG querying the SQLite catalog of 20 experiences
    plus the user's current Markdown taste profile.

    TODO: Connect to the real Gemini API once an API key is configured.
    Currently uses a local keyword-matching fallback.
    """
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Please enter a message.'}), 400

    db = get_db()
    user = db.execute(
        "SELECT * FROM users WHERE id = ?", (session['user_id'],)
    ).fetchone()

    all_exp_rows = db.execute("SELECT * FROM experiences").fetchall()
    all_experiences = [_exp_row_to_dict(row) for row in all_exp_rows]

    api_key = os.environ.get("GEMINI_API_KEY")

    # Fallback simulation if no API key configured
    if not api_key or api_key == "your_gemini_api_key_here":
        # Smart local concierge matching
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
                f"Welcome! Based on your interest, I highly recommend exploring "
                f"**{matched_exp['title']}** in {matched_exp['city']}.\n\n"
                f"It offers a {matched_exp['duration_minutes']}-minute curated journey "
                f"covering {matched_exp['highlights']}.\n\n"
                f"[RECOMMEND: id={matched_exp['id']}, title=\"{matched_exp['title']}\", "
                f"city=\"{matched_exp['city']}\", price={matched_exp['base_price']:.2f}]\n\n"
                f"Would you like me to customize this with an expert docent or audio guide?"
            )
        else:
            ai_response_text = (
                "Welcome! I'm your AI Cultural Concierge. Ask me about Italian cultural "
                "experiences — try mentioning a city like Florence or Rome, or a theme "
                "like Renaissance or Baroque."
            )

        # Update sample preference
        if "florence" in user_message.lower() or "renaissance" in user_message.lower():
            new_prefs = """### Cultural Taste Profile
- **Primary Interests:** Renaissance Masterpieces & Florentine Architecture
- **Visit Pacing:** Dense & Curated (2 hours)
- **Group Style:** Partner / Solo exploration
- **Preferred Perks:** Skip-The-Line Access, Audio Guide
- **Favorite Cities:** Florence, Rome"""
            db.execute(
                "UPDATE users SET preferences = ? WHERE id = ?",
                (new_prefs, session['user_id'])
            )
            db.commit()
            # Re-fetch updated preferences
            user = db.execute(
                "SELECT * FROM users WHERE id = ?", (session['user_id'],)
            ).fetchone()

        return jsonify({
            'response': ai_response_text,
            'updated_profile': user['preferences']
        })

    # TODO: Official Gemini API execution path
    # When the API key is configured, uncomment and implement the Gemini integration.
    return jsonify({'error': 'AI Concierge is not yet configured (no API key).'}), 503


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
