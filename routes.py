"""
routes.py
---------
Main routing blueprint for the application.
Handles page rendering for the home, museums, booking, and the AI concierge guide.
"""
from flask import Blueprint, render_template, request, jsonify, session
from auth import login_required
from models import Museum, Exhibition, Ticket, db
import os
import google.generativeai as genai

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    """
    Renders the landing page.
    """
    return render_template('index.html')

@main_bp.route('/museums')
def museums():
    """
    Renders the museums listing page.
    Fetches all museums from the database to display.
    """
    museums_list = Museum.query.all()
    return render_template('museums.html', museums=museums_list)

@main_bp.route('/booking')
@login_required
def booking():
    """
    Renders the booking page.
    Requires authentication. Allows users to select an exhibition and book a ticket.
    """
    museum_id = request.args.get('museum_id')
    exhibitions_list = Exhibition.query.all()
    return render_template('booking.html', exhibitions=exhibitions_list, preselected_museum=museum_id)

@main_bp.route('/api/book', methods=['POST'])
@login_required
def api_book():
    """
    API endpoint for booking a ticket.
    Receives JSON payload with exhibition_id and creates a Ticket record.
    """
    data = request.json
    exhibition_id = data.get('exhibition_id')
    
    if not exhibition_id:
        return jsonify({'error': 'Missing exhibition selection.'}), 400
        
    exhibition = Exhibition.query.get(exhibition_id)
    if not exhibition:
        return jsonify({'error': 'Invalid exhibition.'}), 404
        
    ticket = Ticket(
        user_id=session.get('user_id'),
        exhibition_id=exhibition.id,
        status='Confirmed'
    )
    db.session.add(ticket)
    db.session.commit()
    
    return jsonify({'success': True, 'message': 'Ticket booked successfully!', 'ticket_id': ticket.id})

@main_bp.route('/guide')
@login_required
def guide():
    """
    Renders the AI Cultural Concierge chat interface.
    Initializes an empty chat history in the session if none exists.
    """
    # If the user accesses the guide, we can optionally clear their history or keep it.
    # We'll keep it as requested: "until the user logs out"
    if 'chat_history' not in session:
        session['chat_history'] = []
    
    return render_template('guide.html')

@main_bp.route('/api/chat', methods=['POST'])
@login_required
def api_chat():
    """
    API endpoint for the AI Cultural Concierge.
    Uses Gemini API and a RAG (Retrieval-Augmented Generation) approach.
    Fetches all Museum and Exhibition data from SQLite to inject as context.
    Maintains a rolling chat history in the user's session cookie.
    """
    data = request.json
    user_message = data.get('message')
    
    if not user_message:
        return jsonify({'error': 'Missing message.'}), 400
        
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return jsonify({'error': 'Gemini API Key is not configured on the server.'}), 500
        
    genai.configure(api_key=api_key)
    
    # 1. Fetch DB Context
    museums = Museum.query.all()
    exhibitions = Exhibition.query.all()
    
    context = "You are a Cultural Concierge, a helpful AI museum guide. Use the following database information to recommend museums and exhibitions to the user:\n\n"
    context += "MUSEUMS:\n"
    for m in museums:
        context += f"- {m.name} (Location: {m.location}): {m.description}\n"
    
    context += "\nCURRENT EXHIBITIONS:\n"
    for e in exhibitions:
        # Assuming e.museum works if backref is set, or we can just list them
        context += f"- '{e.title}' (Start: {e.start_date.strftime('%Y-%m-%d')}, End: {e.end_date.strftime('%Y-%m-%d')})\n"
        
    context += "\nBe polite, highly sophisticated, and concise. You are speaking to a high-end museum visitor. Recommend they book tickets for exhibitions they find interesting."

    # 2. Setup the model
    try:
        model = genai.GenerativeModel(
            model_name='gemini-1.5-flash',
            system_instruction=context
        )
        
        # 3. Handle Chat History
        # We store history in Flask session as [{'role': 'user', 'parts': ['msg']}, ...]
        # Note: Flask session cookies have a 4KB limit. We'll keep only the last 6 messages.
        history = session.get('chat_history', [])
        
        # Start chat with history
        chat = model.start_chat(history=history)
        
        # Send user message
        response = chat.send_message(user_message)
        
        # Update history
        history.append({'role': 'user', 'parts': [user_message]})
        history.append({'role': 'model', 'parts': [response.text]})
        
        # Keep only the last 6 turns (12 messages) to avoid 4KB cookie limit
        session['chat_history'] = history[-12:]
        session.modified = True
        
        return jsonify({'response': response.text})
        
    except Exception as e:
        print(f"Gemini API Error: {e}")
        return jsonify({'error': 'The Concierge is temporarily unavailable.'}), 500
