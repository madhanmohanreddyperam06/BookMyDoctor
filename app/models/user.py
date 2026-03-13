from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from app import db, bcrypt

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(128), nullable=False)
    role = db.Column(db.Enum('admin', 'doctor', 'patient', name='user_role'), nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    admin = db.relationship('Admin', back_populates='user', uselist=False, cascade='all, delete-orphan')
    doctor = db.relationship('Doctor', back_populates='user', uselist=False, cascade='all, delete-orphan')
    patient = db.relationship('Patient', back_populates='user', uselist=False, cascade='all, delete-orphan')
    
    def __init__(self, email, password, role):
        self.email = email
        self.set_password(password)
        self.role = role
    
    def set_password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')
    
    def check_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)
    
    def is_admin(self):
        return self.role == 'admin'
    
    def is_doctor(self):
        return self.role == 'doctor'
    
    def is_patient(self):
        return self.role == 'patient'
    
    def get_profile(self):
        if self.role == 'admin':
            return self.admin
        elif self.role == 'doctor':
            return self.doctor
        elif self.role == 'patient':
            return self.patient
        return None
    
    def __repr__(self):
        return f'<User {self.email} ({self.role})>'
