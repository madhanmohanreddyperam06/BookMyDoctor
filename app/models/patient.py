from datetime import datetime, date
from app import db
from .prescription import Prescription
from .appointment import Appointment

class Patient(db.Model):
    __tablename__ = 'patients'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, unique=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    phone = db.Column(db.String(20))
    date_of_birth = db.Column(db.Date, nullable=False)
    gender = db.Column(db.Enum('male', 'female', 'other', name='gender'), nullable=False)
    address = db.Column(db.Text)
    emergency_contact_name = db.Column(db.String(100))
    emergency_contact_phone = db.Column(db.String(20))
    blood_group = db.Column(db.String(10))
    allergies = db.Column(db.Text)
    medical_history = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    user = db.relationship('User', back_populates='patient')
    appointments = db.relationship('Appointment', back_populates='patient', cascade='all, delete-orphan', lazy='dynamic')
    prescriptions = db.relationship('Prescription', back_populates='patient', cascade='all, delete-orphan', lazy='dynamic')
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"
    
    @property
    def age(self):
        today = date.today()
        return today.year - self.date_of_birth.year - ((today.month, today.day) < (self.date_of_birth.month, self.date_of_birth.day))
    
    def get_upcoming_appointments(self, limit=5):
        from datetime import date
        return self.appointments.filter(
            Appointment.date >= date.today(),
            Appointment.status.in_(['confirmed', 'completed'])
        ).order_by(Appointment.date, Appointment.start_time).limit(limit).all()
    
    def get_past_appointments(self, limit=10):
        from datetime import date
        return self.appointments.filter(
            Appointment.date < date.today()
        ).order_by(Appointment.date.desc(), Appointment.start_time.desc()).limit(limit).all()
    
    def get_medical_history_summary(self):
        return self.prescriptions.order_by(Prescription.created_at.desc()).limit(5).all()
    
    def __repr__(self):
        return f'<Patient {self.full_name}>'
