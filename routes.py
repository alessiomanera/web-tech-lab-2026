"""
routes.py
---------
Main routing blueprint for the Museum & Cultural Experience platform.
Handles page rendering for Home, Explore Experiences, 4-Step Booking Wizard,
the AI Cultural Concierge, User Profile Dashboard, and asynchronous REST APIs.
"""
import os
import random
import string
import json
from datetime import datetime
from flask import Blueprint, render_template, request, jsonify, session, redirect, url_for, flash
from auth import login_required
from models import db, Museum, Exhibition, Experience, Booking, User
import google.generativeai as genai

main_bp = Blueprint('main', __name__)

def generate_booking_code():
    """Generates a memorable unique booking reference code, e.g., EXP-2026-A91F."""
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=4))
    return f"EXP-2026-{suffix}"

# -----------------------------------------------------------------------------
# 1. Page Navigation Routes
# -----------------------------------------------------------------------------

@main_bp.route('/')
def home():
    """
    Renders the main cultural portal landing page.
    Displays hero section, 3-step value workflow, and top featured experiences.
    """
    featured_experiences = Experience.query.filter_by(is_featured=True).limit(4).all()
    if not featured_experiences:
        featured_experiences = Experience.query.limit(4).all()
    return render_template('index.html', featured=featured_experiences)


@main_bp.route('/experiences')
def experiences():
    """
    Renders the full 20-Experience catalog.
    Supports filtering by city, theme, and search keyword.
    """
    city_filter = request.args.get('city')
    theme_filter = request.args.get('theme')
    search_query = request.args.get('q')

    query = Experience.query

    if city_filter and city_filter.lower() != 'all':
        query = query.filter(Experience.city.ilike(f"%{city_filter}%"))

    if theme_filter and theme_filter.lower() != 'all':
        query = query.filter(Experience.theme.ilike(f"%{theme_filter}%"))

    if search_query:
        query = query.filter(
            (Experience.title.ilike(f"%{search_query}%")) |
            (Experience.city.ilike(f"%{search_query}%")) |
            (Experience.description.ilike(f"%{search_query}%"))
        )

    all_experiences = query.all()
    
    # Get distinct cities and themes for filter pills
    cities = ['All', 'Florence', 'Rome', 'Venice', 'Milan', 'Turin', 'Naples', 'Verona', 'Palermo', 'Bologna']
    
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
    exp = Experience.query.get_or_404(exp_id)
    return render_template('experience_detail.html', exp=exp)


@main_bp.route('/booking')
@login_required
def booking():
    """
    Renders the 4-step Frictionless Booking Wizard.
    Pre-selects experience if passed via ?exp_id=X.
    """
    preselected_id = request.args.get('exp_id')
    all_experiences = Experience.query.all()
    
    selected_exp = None
    if preselected_id:
        try:
            selected_exp = Experience.query.get(int(preselected_id))
        except (ValueError, TypeError):
            selected_exp = None

    user = User.query.get(session['user_id'])
    
    return render_template(
        'booking.html',
        experiences=all_experiences,
        selected_exp=selected_exp,
        user=user
    )


@main_bp.route('/concierge')
@login_required
def concierge():
    """
    Renders the AI Cultural Concierge interactive chat interface.
    Loads the user's live Markdown Cultural Taste Profile from SQLite.
    """
    user = User.query.get(session['user_id'])
    if 'chat_history' not in session:
        session['chat_history'] = []

    return render_template('guide.html', user=user)


# Backward compatibility route
@main_bp.route('/guide')
def guide_redirect():
    return redirect(url_for('main.concierge'))

@main_bp.route('/museums')
def museums_redirect():
    return redirect(url_for('main.experiences'))


@main_bp.route('/profile')
@login_required
def profile():
    """
    Renders the user account dashboard with active digital passes,
    past visit history, review submission forms, and the live Cultural Taste Profile.
    """
    user = User.query.get(session['user_id'])
    bookings = Booking.query.filter_by(user_id=user.id).order_by(Booking.booking_date.desc()).all()
    
    return render_template('profile.html', user=user, bookings=bookings)


# -----------------------------------------------------------------------------
# 2. REST API Endpoints
# -----------------------------------------------------------------------------

@main_bp.route('/api/book', methods=['POST'])
@login_required
def api_book():
    """
    API endpoint for confirming a cultural booking.
    Receives experience_id, visit_date, time_slot, guests_count, and selected_addons.
    Calculates total price, creates Booking record in SQLite, and returns confirmation.
    """
    data = request.get_json() or {}
    exp_id = data.get('experience_id')
    visit_date_str = data.get('visit_date')
    time_slot = data.get('time_slot')
    guests_count = int(data.get('guests_count', 1))
    selected_addons = data.get('selected_addons', [])

    if not exp_id or not visit_date_str or not time_slot:
        return jsonify({'error': 'Please select an experience, visit date, and time slot.'}), 400

    exp = Experience.query.get(exp_id)
    if not exp:
        return jsonify({'error': 'Selected experience not found.'}), 404

    try:
        visit_date = datetime.strptime(visit_date_str, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({'error': 'Invalid date format. Expected YYYY-MM-DD.'}), 400

    # Calculate total price
    base_total = exp.base_price * guests_count
    addons_total = sum(float(a.get('price', 0)) for a in selected_addons) * guests_count
    total_price = base_total + addons_total

    booking_code = generate_booking_code()

    new_booking = Booking(
        booking_code=booking_code,
        user_id=session['user_id'],
        experience_id=exp.id,
        visit_date=visit_date,
        time_slot=time_slot,
        guests_count=guests_count,
        selected_addons_json=json.dumps(selected_addons),
        total_price=total_price,
        status='Confirmed'
    )

    db.session.add(new_booking)
    db.session.commit()

    return jsonify({
        'success': True,
        'message': 'Experience booked successfully!',
        'booking_code': booking_code,
        'total_price': f"€{total_price:.2f}",
        'experience_title': exp.title,
        'city': exp.city,
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

    booking_record = Booking.query.filter_by(id=booking_id, user_id=session['user_id']).first()
    if not booking_record:
        return jsonify({'error': 'Booking not found.'}), 404

    booking_record.feedback_rating = int(rating)
    booking_record.feedback_text = comment
    booking_record.feedback_date = datetime.utcnow()
    db.session.commit()

    return jsonify({'success': True, 'message': 'Thank you for your feedback!'})


@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    AI Cultural Concierge endpoint.
    Performs grounded RAG querying SQLite catalog of 20 experiences + user's current Markdown taste profile.
    Extracts new visitor preferences in background and updates User.preferences in SQLite.
    """
    data = request.get_json() or {}
    user_message = data.get('message', '').strip()

    if not user_message:
        return jsonify({'error': 'Please enter a message.'}), 400

    user = User.query.get(session['user_id'])
    all_experiences = Experience.query.all()

    # Build Grounded Catalog Context
    catalog_context = "AVAILABLE PRE-CONFIGURED CULTURAL EXPERIENCES (ITALY):\n"
    for exp in all_experiences:
        catalog_context += (
            f"- [ID: {exp.id}] {exp.title} in {exp.city} (Theme: {exp.theme}, Duration: {exp.duration_minutes}m, "
            f"Base Price: €{exp.base_price:.2f}, Badge: '{exp.badge}'). Highlights: {exp.highlights}\n"
        )

    user_profile_context = user.preferences or "No prior taste profile recorded."

    system_instruction = f"""You are the AI Cultural Concierge for Italy's premier cultural experience platform.
Your mission is to understand visitor tastes, recommend the best pre-configured cultural packages from our database, and assist in tailoring their itinerary.

{catalog_context}

CURRENT VISITOR CULTURAL TASTE PROFILE:
{user_profile_context}

RULES:
1. Ground your recommendations strictly in the experiences listed above.
2. Be sophisticated, warmly hospitable, and concise.
3. Whenever you recommend a specific experience, include a special actionable card trigger on its own line in this exact format:
[RECOMMEND: id=X, title="Title", city="City", price=Price]
4. Do not invent non-existent packages or ticket prices.
"""

    api_key = os.environ.get("GEMINI_API_KEY")

    # Fallback simulation if no API key configured
    if not api_key or api_key == "your_gemini_api_key_here":
        # Smart local concierge matching
        matched_exp = None
        for exp in all_experiences:
            if exp.city.lower() in user_message.lower() or exp.theme.lower() in user_message.lower():
                matched_exp = exp
                break
        if not matched_exp:
            matched_exp = all_experiences[0]

        ai_response_text = (
            f"Welcome! Based on your interest, I highly recommend exploring **{matched_exp.title}** in {matched_exp.city}.\n\n"
            f"It offers a {matched_exp.duration_minutes}-minute curated journey covering {matched_exp.highlights}.\n\n"
            f"[RECOMMEND: id={matched_exp.id}, title=\"{matched_exp.title}\", city=\"{matched_exp.city}\", price={matched_exp.base_price:.2f}]\n\n"
            f"Would you like me to customize this with an expert docent or audio guide?"
        )

        # Update sample preference
        if "florence" in user_message.lower() or "renaissance" in user_message.lower():
            user.preferences = """### Cultural Taste Profile
- **Primary Interests:** Renaissance Masterpieces & Florentine Architecture
- **Visit Pacing:** Dense & Curated (2 hours)
- **Group Style:** Partner / Solo exploration
- **Preferred Perks:** Skip-The-Line Access, Audio Guide
- **Favorite Cities:** Florence, Rome"""
            db.session.commit()

        return jsonify({'response': ai_response_text, 'updated_profile': user.preferences})

    # Official Gemini API Execution
    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=system_instruction
        )

        history = session.get('chat_history', [])
        chat = model.start_chat(history=history)
        response = chat.send_message(user_message)
        ai_text = response.text

        # Update session chat history
        history.append({'role': 'user', 'parts': [user_message]})
        history.append({'role': 'model', 'parts': [ai_text]})
        session['chat_history'] = history[-10:] # Keep last 10 messages
        session.modified = True

        # Background Memory Extraction Pipeline
        try:
            memory_extractor_prompt = f"""Based on this user message: "{user_message}" and existing profile:
"{user_profile_context}"
Summarize the user's ongoing art/cultural tastes into a concise Markdown profile (Interests, Pacing, Group Style, Perks, Favorite Cities).
Output ONLY the Markdown block starting with '### Cultural Taste Profile'."""
            memory_model = genai.GenerativeModel('gemini-1.5-flash')
            mem_res = memory_model.generate_content(memory_extractor_prompt)
            if mem_res.text and "### Cultural Taste Profile" in mem_res.text:
                user.preferences = mem_res.text.strip()
                db.session.commit()
        except Exception as mem_err:
            print(f"Memory extraction non-critical error: {mem_err}")

        return jsonify({'response': ai_text, 'updated_profile': user.preferences})

    except Exception as e:
        print(f"Gemini API Error: {e}")
        return jsonify({'error': 'The Concierge is temporarily unavailable.'}), 500


@main_bp.route('/api/profile/reset-memory', methods=['POST'])
@login_required
def api_reset_memory():
    """Resets the user's AI Cultural Taste Profile to default."""
    user = User.query.get(session['user_id'])
    user.preferences = None
    db.session.commit()
    return jsonify({'success': True, 'message': 'Taste profile reset successfully.'})
