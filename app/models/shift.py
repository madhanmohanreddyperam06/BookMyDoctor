from datetime import datetime, time, date
from app import db

class Shift(db.Model):
    __tablename__ = 'shifts'
    
    id = db.Column(db.Integer, primary_key=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    date = db.Column(db.Date, nullable=False, index=True)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    shift_type = db.Column(db.Enum('morning', 'evening', 'night', name='shift_type'), nullable=False)
    consultation_mode = db.Column(db.Enum('online', 'offline', name='consultation_mode'), nullable=False)
    max_patients = db.Column(db.Integer, default=1, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    doctor = db.relationship('Doctor', back_populates='shifts')
    slots = db.relationship('Slot', back_populates='shift', cascade='all, delete-orphan', lazy='dynamic')
    
    # Composite index for efficient querying
    __table_args__ = (
        db.Index('idx_shift_doctor_date', 'doctor_id', 'date', 'consultation_mode'),
        db.UniqueConstraint('doctor_id', 'date', 'start_time', 'consultation_mode', name='unique_shift_time'),
    )
    
    @property
    def duration_minutes(self):
        start = datetime.combine(date.min, self.start_time)
        end = datetime.combine(date.min, self.end_time)
        return int((end - start).total_seconds() / 60)
    
    @property
    def shift_display(self):
        return f"{self.shift_type.title()} ({self.start_time.strftime('%H:%M')} - {self.end_time.strftime('%H:%M')})"
    
    def get_available_slots(self):
        return self.slots.filter_by(is_booked=False).order_by(Slot.start_time).all()
    
    def get_booked_slots(self):
        return self.slots.filter_by(is_booked=True).order_by(Slot.start_time).all()
    
    def get_booked_count(self):
        return self.slots.filter_by(is_booked=True).count()
    
    def is_available_for_booking(self):
        return self.is_active and self.date >= date.today()
    
    def __repr__(self):
        return f'<Shift {self.doctor.full_name} - {self.date} {self.shift_type} ({self.consultation_mode})>'
