from datetime import datetime
from app import db
from .appointment import Appointment

class Doctor(db.Model):
    __tablename__ = 'doctors'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    speciality_id = db.Column(db.Integer, db.ForeignKey('specialities.id'), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    consultation_mode = db.Column(db.Enum('online', 'offline', name='consultation_mode'), nullable=False)
    consultation_fee = db.Column(db.Numeric(10, 2), nullable=False)
    experience_years = db.Column(db.Integer)
    qualifications = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='doctor')
    speciality = db.relationship('Speciality', back_populates='doctors')
    shifts = db.relationship('Shift', back_populates='doctor', cascade='all, delete-orphan', lazy='dynamic')
    appointments = db.relationship('Appointment', back_populates='doctor', cascade='all, delete-orphan', lazy='dynamic')
    prescriptions = db.relationship('Prescription', back_populates='doctor', cascade='all, delete-orphan', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"Dr. {self.first_name} {self.last_name}"
    
    def get_active_shifts(self):
        return self.shifts.filter_by(is_active=True).order_by(Shift.date, Shift.start_time)
    
    def get_upcoming_appointments(self, limit=10):
        from datetime import date
        return self.appointments.filter(
            Appointment.date >= date.today(),
            Appointment.status.in_(['confirmed', 'completed'])
        ).order_by(Appointment.date, Appointment.start_time).limit(limit).all()
    
    def get_today_appointments(self):
        from datetime import date
        return self.appointments.filter(
            Appointment.date == date.today()
        ).order_by(Appointment.start_time).all()
    
    def __repr__(self):
        return f'<Doctor {self.full_name} ({self.consultation_mode})>'
