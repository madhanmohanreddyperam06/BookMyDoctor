from datetime import datetime
from app import db

class Medicine(db.Model):
    __tablename__ = 'medicines'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, index=True)
    generic_name = db.Column(db.String(100))
    brand_name = db.Column(db.String(100))
    dosage_form = db.Column(db.Enum('tablet', 'capsule', 'syrup', 'injection', 'ointment', 'drops', 'inhaler', 'other', name='dosage_form'))
    strength = db.Column(db.String(50))  # e.g., "500mg", "10ml"
    description = db.Column(db.Text)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    
    # Relationships
    prescription_items = db.relationship('PrescriptionItem', back_populates='medicine', lazy='dynamic')
    
    def __init__(self, name, generic_name=None, brand_name=None, dosage_form=None, strength=None, description=None):
        self.name = name
        self.generic_name = generic_name
        self.brand_name = brand_name
        self.dosage_form = dosage_form
        self.strength = strength
        self.description = description
    
    @property
    def display_name(self):
        parts = [self.name]
        if self.strength:
            parts.append(self.strength)
        if self.dosage_form:
            parts.append(self.dosage_form.title())
        return ' '.join(parts)
    
    @classmethod
    def search_medicines(cls, query_text, limit=20):
        """Search medicines by name, generic name, or brand name"""
        return cls.query.filter(
            cls.is_active == True,
            db.or_(
                cls.name.ilike(f'%{query_text}%'),
                cls.generic_name.ilike(f'%{query_text}%'),
                cls.brand_name.ilike(f'%{query_text}%')
            )
        ).limit(limit).all()
    
    def __repr__(self):
        return f'<Medicine {self.display_name}>'
