from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from app import db
from app.models import User, Doctor, Patient, Shift, Slot, Appointment, Prescription
from datetime import datetime, date, timedelta

doctor = Blueprint('doctor', __name__)

# Doctor access decorator
def doctor_required(f):
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_doctor():
            flash('Doctor access required.', 'danger')
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@doctor.route('/dashboard')
@login_required
@doctor_required
def dashboard():
    """Doctor dashboard"""
    doctor_profile = current_user.doctor
    
    # Get today's appointments
    today_appointments = doctor_profile.get_today_appointments()
    
    # Get upcoming appointments
    upcoming_appointments = doctor_profile.get_upcoming_appointments(limit=5)
    
    # Get this week's shifts
    start_of_week = date.today() - timedelta(days=date.today().weekday())
    end_of_week = start_of_week + timedelta(days=6)
    
    week_shifts = Shift.query.filter(
        Shift.doctor_id == doctor_profile.id,
        Shift.date >= start_of_week,
        Shift.date <= end_of_week,
        Shift.is_active == True
    ).order_by(Shift.date, Shift.start_time).all()
    
    return render_template('doctor/dashboard.html',
                         doctor=doctor_profile,
                         today_appointments=today_appointments,
                         upcoming_appointments=upcoming_appointments,
                         week_shifts=week_shifts)

@doctor.route('/schedule')
@login_required
@doctor_required
def schedule():
    """View doctor's schedule"""
    doctor_profile = current_user.doctor
    
    # Get date range for viewing
    start_date = request.args.get('start_date')
    if start_date:
        start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
    else:
        start_date = date.today()
    
    end_date = start_date + timedelta(days=6)  # Show one week
    
    shifts = Shift.query.filter(
        Shift.doctor_id == doctor_profile.id,
        Shift.date >= start_date,
        Shift.date <= end_date,
        Shift.is_active == True
    ).order_by(Shift.date, Shift.start_time).all()
    
    return render_template('doctor/schedule.html',
                         doctor=doctor_profile,
                         shifts=shifts,
                         start_date=start_date,
                         end_date=end_date)

@doctor.route('/appointments')
@login_required
@doctor_required
def appointments():
    """View doctor's appointments"""
    doctor_profile = current_user.doctor
    page = request.args.get('page', 1, type=int)
    status_filter = request.args.get('status')
    
    query = Appointment.query.filter_by(doctor_id=doctor_profile.id)
    
    if status_filter:
        query = query.filter_by(status=status_filter)
    
    appointments = query.order_by(Appointment.date.desc(), Appointment.start_time.desc()).paginate(
        page=page, per_page=10, error_out=False)
    
    return render_template('doctor/appointments.html',
                         doctor=doctor_profile,
                         appointments=appointments,
                         status_filter=status_filter)

@doctor.route('/appointment/<int:appointment_id>')
@login_required
@doctor_required
def appointment_detail(appointment_id):
    """View appointment details"""
    doctor_profile = current_user.doctor
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=doctor_profile.id
    ).first_or_404()
    
    return render_template('doctor/appointment_detail.html',
                         doctor=doctor_profile,
                         appointment=appointment)

@doctor.route('/appointment/<int:appointment_id>/update_status', methods=['POST'])
@login_required
@doctor_required
def update_appointment_status(appointment_id):
    """Update appointment status"""
    doctor_profile = current_user.doctor
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=doctor_profile.id
    ).first_or_404()
    
    new_status = request.form.get('status')
    
    if new_status in ['confirmed', 'completed', 'cancelled', 'no_show']:
        if new_status == 'completed':
            appointment.complete_appointment()
        elif new_status == 'cancelled':
            appointment.cancel_appointment()
        elif new_status == 'no_show':
            appointment.mark_no_show()
        else:
            appointment.status = new_status
            db.session.add(appointment)
            db.session.commit()
        
        flash(f'Appointment status updated to {new_status.replace("_", " ").title()}', 'success')
    else:
        flash('Invalid status', 'danger')
    
    return redirect(url_for('doctor.appointment_detail', appointment_id=appointment_id))

@doctor.route('/appointment/<int:appointment_id>/prescription', methods=['GET', 'POST'])
@login_required
@doctor_required
def manage_prescription(appointment_id):
    """Manage prescription for appointment"""
    doctor_profile = current_user.doctor
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=doctor_profile.id
    ).first_or_404()
    
    if request.method == 'POST':
        diagnosis = request.form.get('diagnosis')
        symptoms = request.form.get('symptoms')
        notes = request.form.get('notes')
        follow_up_instructions = request.form.get('follow_up_instructions')
        follow_up_date = request.form.get('follow_up_date')
        
        # Create or update prescription
        if appointment.prescription:
            prescription = appointment.prescription
            prescription.diagnosis = diagnosis
            prescription.symptoms = symptoms
            prescription.notes = notes
            prescription.follow_up_instructions = follow_up_instructions
            prescription.follow_up_date = datetime.strptime(follow_up_date, '%Y-%m-%d').date() if follow_up_date else None
        else:
            prescription = Prescription(
                appointment_id=appointment.id,
                doctor_id=doctor_profile.id,
                patient_id=appointment.patient_id,
                diagnosis=diagnosis,
                symptoms=symptoms,
                notes=notes,
                follow_up_instructions=follow_up_instructions,
                follow_up_date=datetime.strptime(follow_up_date, '%Y-%m-%d').date() if follow_up_date else None
            )
            db.session.add(prescription)
        
        db.session.commit()
        flash('Prescription saved successfully!', 'success')
        return redirect(url_for('doctor.appointment_detail', appointment_id=appointment_id))
    
    return render_template('doctor/prescription.html',
                         doctor=doctor_profile,
                         appointment=appointment)

@doctor.route('/appointment/<int:appointment_id>/video_link', methods=['POST'])
@login_required
@doctor_required
def add_video_link(appointment_id):
    """Add video consultation link"""
    doctor_profile = current_user.doctor
    appointment = Appointment.query.filter_by(
        id=appointment_id,
        doctor_id=doctor_profile.id
    ).first_or_404()
    
    video_link = request.form.get('video_link')
    
    if appointment.add_video_link(video_link):
        flash('Video link added successfully!', 'success')
    else:
        flash('Failed to add video link. This might be an offline appointment.', 'danger')
    
    return redirect(url_for('doctor.appointment_detail', appointment_id=appointment_id))
