from datetime import datetime
from app import db

class Prescription(db.Model):
    __tablename__ = 'prescriptions'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False, unique=True)
    doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'), nullable=False)
    patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'), nullable=False)
    diagnosis = db.Column(db.Text, nullable=False)
    symptoms = db.Column(db.Text)
    notes = db.Column(db.Text)
    follow_up_instructions = db.Column(db.Text)
    follow_up_date = db.Column(db.Date)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    appointment = db.relationship('Appointment', back_populates='prescription')
    doctor = db.relationship('Doctor', back_populates='prescriptions')
    patient = db.relationship('Patient', back_populates='prescriptions')
    medicines = db.relationship('PrescriptionItem', back_populates='prescription', cascade='all, delete-orphan', lazy='dynamic')
    
    def add_medicine(self, medicine, dosage, frequency, duration, instructions=None):
        """Add medicine to prescription"""
        prescription_item = PrescriptionItem(
            prescription_id=self.id,
            medicine_id=medicine.id,
            dosage=dosage,
            frequency=frequency,
            duration=duration,
            instructions=instructions
        )
        db.session.add(prescription_item)
        return prescription_item
    
    def remove_medicine(self, medicine_id):
        """Remove medicine from prescription"""
        medicine_item = self.medicines.filter_by(medicine_id=medicine_id).first()
        if medicine_item:
            db.session.delete(medicine_item)
            return True
        return False
    
    def get_medicines_list(self):
        """Get list of medicines in prescription"""
        return self.medicines.order_by(PrescriptionItem.created_at).all()
    
    @property
    def medicines_count(self):
        return self.medicines.count()
    
    def __repr__(self):
        return f'<Prescription for {self.patient.full_name} by {self.doctor.full_name} on {self.created_at.date()}>'

class PrescriptionItem(db.Model):
    __tablename__ = 'prescription_items'
    
    id = db.Column(db.Integer, primary_key=True)
    prescription_id = db.Column(db.Integer, db.ForeignKey('prescriptions.id'), nullable=False)
    medicine_id = db.Column(db.Integer, db.ForeignKey('medicines.id'), nullable=False)
    dosage = db.Column(db.String(50), nullable=False)  # e.g., "1 tablet", "5ml"
    frequency = db.Column(db.String(100), nullable=False)  # e.g., "Twice daily", "After meals"
    duration = db.Column(db.String(50), nullable=False)  # e.g., "7 days", "2 weeks"
    instructions = db.Column(db.Text)  # Additional instructions
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    
    # Relationships
    prescription = db.relationship('Prescription', back_populates='medicines')
    medicine = db.relationship('Medicine', back_populates='prescription_items')
    
    @property
    def full_instruction(self):
        parts = [self.dosage, self.frequency, self.duration]
        if self.instructions:
            parts.append(f"({self.instructions})")
        return ' - '.join(parts)
    
    def __repr__(self):
        return f'<PrescriptionItem {self.medicine.name} - {self.full_instruction}>'
