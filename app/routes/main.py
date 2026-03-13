from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user

main = Blueprint('main', __name__)

@main.route('/')
def index():
    """Home page"""
    if current_user.is_authenticated:
        if current_user.is_admin():
            return redirect(url_for('admin.dashboard'))
        elif current_user.is_doctor():
            return redirect(url_for('doctor.dashboard'))
        elif current_user.is_patient():
            return redirect(url_for('patient.dashboard'))
    
    return render_template('auth/landing.html')

@main.route('/about')
def about():
    """About page"""
    return render_template('about.html')

@main.route('/contact')
def contact():
    """Contact page"""
    return render_template('contact.html')
