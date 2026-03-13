from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import Appointment
from datetime import datetime, timedelta

video = Blueprint('video', __name__)

@video.route('/consultation/<int:appointment_id>')
@login_required
def video_consultation(appointment_id):
    """Video consultation page"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Check if user has access to this appointment
    if current_user.is_doctor():
        if appointment.doctor_id != current_user.doctor.id:
            flash('You do not have access to this appointment', 'danger')
            return redirect(url_for('doctor.dashboard'))
    elif current_user.is_patient():
        if appointment.patient_id != current_user.patient.id:
            flash('You do not have access to this appointment', 'danger')
            return redirect(url_for('patient.dashboard'))
    else:
        flash('Invalid access', 'danger')
        return redirect(url_for('main.index'))
    
    # Check if appointment is confirmed and within consultation time
    now = datetime.utcnow()
    appointment_datetime = datetime.combine(appointment.date, appointment.start_time)
    
    # Allow access 30 minutes before appointment time
    if appointment.status != 'confirmed' or now < appointment_datetime - timedelta(minutes=30):
        flash('Video consultation is not available at this time', 'warning')
        return redirect(url_for('doctor.appointment_detail' if current_user.is_doctor() else 'patient.appointment_detail', 
                               appointment_id=appointment.id))
    
    # Check if it's too late (2 hours after appointment time)
    if now > appointment_datetime + timedelta(hours=2):
        flash('Video consultation period has ended', 'warning')
        return redirect(url_for('doctor.appointment_detail' if current_user.is_doctor() else 'patient.appointment_detail', 
                               appointment_id=appointment.id))
    
    # Check if consultation mode is online
    if appointment.consultation_mode != 'online':
        flash('This is not an online consultation', 'warning')
        return redirect(url_for('doctor.appointment_detail' if current_user.is_doctor() else 'patient.appointment_detail', 
                               appointment_id=appointment.id))
    
    return render_template('video_consultation.html', appointment=appointment)

@video.route('/consultation/<int:appointment_id>/start', methods=['POST'])
@login_required
def start_consultation(appointment_id):
    """Start video consultation (AJAX endpoint)"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify access
    if current_user.is_doctor() and appointment.doctor_id != current_user.doctor.id:
        return {'success': False, 'message': 'Access denied'}, 403
    elif current_user.is_patient() and appointment.patient_id != current_user.patient.id:
        return {'success': False, 'message': 'Access denied'}, 403
    
    # In a real implementation, this would:
    # 1. Generate a unique room ID
    # 2. Create video session using WebRTC/Jitsi
    # 3. Return session details
    
    room_id = f"room_{appointment.id}_{int(datetime.utcnow().timestamp())}"
    
    return {
        'success': True,
        'room_id': room_id,
        'appointment_id': appointment.id,
        'participant_name': current_user.doctor.full_name if current_user.is_doctor() else current_user.patient.full_name
    }

@video.route('/consultation/<int:appointment_id>/end', methods=['POST'])
@login_required
def end_consultation(appointment_id):
    """End video consultation (AJAX endpoint)"""
    appointment = Appointment.query.get_or_404(appointment_id)
    
    # Verify access (only doctor can end consultation)
    if not current_user.is_doctor() or appointment.doctor_id != current_user.doctor.id:
        return {'success': False, 'message': 'Access denied'}, 403
    
    # Mark appointment as completed
    if appointment.status == 'confirmed':
        appointment.status = 'completed'
        appointment.payment_status = 'paid'
        db.session.commit()
    
    return {
        'success': True,
        'message': 'Consultation ended successfully',
        'redirect_url': url_for('doctor.appointment_detail', appointment_id=appointment.id)
    }
