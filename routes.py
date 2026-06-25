from flask import Blueprint, render_template

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def home():
    return render_template('index.html')

@main_bp.route('/museums')
def museums():
    # Placeholder: In the future, fetch museums from db
    return render_template('museums.html')

@main_bp.route('/booking')
def booking():
    return render_template('booking.html')

@main_bp.route('/guide')
def guide():
    # Placeholder for AI Guide page
    return render_template('base.html') # Temp fallback
