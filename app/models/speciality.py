from datetime import datetime
from app import db

class Speciality(db.Model):
    __tablename__ = 'specialities'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False, index=True)
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    doctors = db.relationship('Doctor', back_populates='speciality', lazy='dynamic')
    
    def __init__(self, name, description=None):
        self.name = name
        self.description = description
    
    def get_active_doctors_count(self):
        return self.doctors.filter_by(is_active=True).count()
    
    def __repr__(self):
        return f'<Speciality {self.name}>'
