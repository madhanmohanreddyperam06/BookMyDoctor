#!/usr/bin/env python3
"""
Initialize SQLite database for Doctor Appointment System
"""

import os
import sys
from datetime import datetime, date, timedelta

# Add the project root to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Admin, Doctor, Patient, Speciality, Shift, Slot, Appointment, Prescription, Medicine

def init_database():
    """Initialize the database with sample data"""
    app = create_app()
    
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        
        # Check if data already exists
        if Speciality.query.count() > 0:
            print("⚠️  Database already contains data!")
            print("📊 Current data:")
            print(f"   Users: {User.query.count()}")
            print(f"   Admins: {Admin.query.count()}")
            print(f"   Doctors: {Doctor.query.count()}")
            print(f"   Patients: {Patient.query.count()}")
            print(f"   Specialities: {Speciality.query.count()}")
            print(f"   Medicines: {Medicine.query.count()}")
            
            choice = input("\nDo you want to reset the database? (y/N): ").lower()
            if choice != 'y':
                print("❌ Database initialization cancelled.")
                return
            
            # Clear existing data
            print("🗑️  Clearing existing data...")
            db.session.query(Appointment).delete()
            db.session.query(Prescription).delete()
            db.session.query(Slot).delete()
            db.session.query(Shift).delete()
            db.session.query(Medicine).delete()
            db.session.query(Patient).delete()
            db.session.query(Doctor).delete()
            db.session.query(Admin).delete()
            db.session.query(Speciality).delete()
            db.session.query(User).delete()
            db.session.commit()
        
        # Create specialities
        print("Creating specialities...")
        specialities = [
            Speciality(name='General Medicine', description='General medical consultation and primary care'),
            Speciality(name='Cardiology', description='Heart and cardiovascular diseases'),
            Speciality(name='Pediatrics', description='Medical care for children and infants'),
            Speciality(name='Orthopedics', description='Bone and joint disorders'),
            Speciality(name='Dermatology', description='Skin diseases and conditions')
        ]
        
        for speciality in specialities:
            db.session.add(speciality)
        db.session.commit()
        
        # Create medicines
        print("Creating medicines...")
        medicines = [
            Medicine(name='Paracetamol', generic_name='Acetaminophen', dosage_form='Tablet', strength='500mg'),
            Medicine(name='Ibuprofen', generic_name='Ibuprofen', dosage_form='Tablet', strength='400mg'),
            Medicine(name='Amoxicillin', generic_name='Amoxicillin', dosage_form='Capsule', strength='500mg'),
            Medicine(name='Omeprazole', generic_name='Omeprazole', dosage_form='Capsule', strength='20mg'),
            Medicine(name='Salbutamol', generic_name='Albuterol', dosage_form='Inhaler', strength='100mcg')
        ]
        
        for medicine in medicines:
            db.session.add(medicine)
        db.session.commit()
        
        # Create admin user
        print("Creating admin user...")
        admin_user = User(email='admin@hospital.com', password='admin123', role='admin')
        db.session.add(admin_user)
        db.session.flush()  # Get the ID without committing
        
        admin_profile = Admin(user_id=admin_user.id, first_name='System', last_name='Administrator', 
                             phone='123-456-7890')
        db.session.add(admin_profile)
        db.session.commit()
        
        # Create sample doctors
        print("Creating doctors...")
        doctors_data = [
            {
                'email': 'dr.smith@hospital.com',
                'password': 'smith123',
                'first_name': 'John',
                'last_name': 'Smith',
                'phone': '555-0101',
                'consultation_mode': 'online',
                'consultation_fee': 150.00,
                'speciality_name': 'General Medicine',
                'qualifications': 'MD, General Practitioner'
            },
            {
                'email': 'dr.johnson@hospital.com',
                'password': 'johnson123',
                'first_name': 'Sarah',
                'last_name': 'Johnson',
                'phone': '555-0102',
                'consultation_mode': 'offline',
                'consultation_fee': 120.00,
                'speciality_name': 'Cardiology',
                'qualifications': 'MD, Cardiologist'
            },
            {
                'email': 'dr.wilson@hospital.com',
                'password': 'wilson123',
                'first_name': 'Michael',
                'last_name': 'Wilson',
                'phone': '555-0103',
                'consultation_mode': 'online',
                'consultation_fee': 180.00,
                'speciality_name': 'Pediatrics',
                'qualifications': 'MD, Pediatrician'
            },
            {
                'email': 'dr.brown@hospital.com',
                'password': 'brown123',
                'first_name': 'Emily',
                'last_name': 'Brown',
                'phone': '555-0104',
                'consultation_mode': 'offline',
                'consultation_fee': 200.00,
                'speciality_name': 'Orthopedics',
                'qualifications': 'MD, Orthopedic Surgeon'
            },
            {
                'email': 'dr.davis@hospital.com',
                'password': 'davis123',
                'first_name': 'Robert',
                'last_name': 'Davis',
                'phone': '555-0105',
                'consultation_mode': 'online',
                'consultation_fee': 160.00,
                'speciality_name': 'Dermatology',
                'qualifications': 'MD, Dermatologist'
            }
        ]
        
        for doc_data in doctors_data:
            # Create user account
            doctor_user = User(email=doc_data['email'], password=doc_data['password'], role='doctor')
            db.session.add(doctor_user)
            db.session.flush()
            
            # Find speciality
            speciality = Speciality.query.filter_by(name=doc_data['speciality_name']).first()
            
            # Create doctor profile
            doctor = Doctor(
                user_id=doctor_user.id,
                first_name=doc_data['first_name'],
                last_name=doc_data['last_name'],
                phone=doc_data['phone'],
                consultation_mode=doc_data['consultation_mode'],
                consultation_fee=doc_data['consultation_fee'],
                speciality_id=speciality.id if speciality else 1,
                qualifications=doc_data['qualifications'],
                experience_years=10,
                is_active=True
            )
            db.session.add(doctor)
        
        db.session.commit()
        
        # Create sample patients
        print("Creating patients...")
        patients_data = [
            {
                'email': 'patient1@email.com',
                'password': 'patient123',
                'first_name': 'Alice',
                'last_name': 'Johnson',
                'phone': '555-1001',
                'date_of_birth': date(1985, 5, 15),
                'gender': 'female'
            },
            {
                'email': 'patient2@email.com',
                'password': 'patient123',
                'first_name': 'Bob',
                'last_name': 'Smith',
                'phone': '555-1002',
                'date_of_birth': date(1990, 8, 22),
                'gender': 'male'
            },
            {
                'email': 'patient3@email.com',
                'password': 'patient123',
                'first_name': 'Carol',
                'last_name': 'Williams',
                'phone': '555-1003',
                'date_of_birth': date(1978, 12, 3),
                'gender': 'female'
            }
        ]
        
        for pat_data in patients_data:
            # Create user account
            patient_user = User(email=pat_data['email'], password=pat_data['password'], role='patient')
            db.session.add(patient_user)
            db.session.flush()
            
            # Create patient profile
            patient = Patient(
                user_id=patient_user.id,
                first_name=pat_data['first_name'],
                last_name=pat_data['last_name'],
                phone=pat_data['phone'],
                date_of_birth=pat_data['date_of_birth'],
                gender=pat_data['gender'],
                blood_group='O+',
                medical_history='No significant medical history',
                allergies='None known'
            )
            db.session.add(patient)
        
        db.session.commit()
        
        # Create sample shifts
        print("Creating sample shifts...")
        doctors = Doctor.query.all()
        
        for i, doctor in enumerate(doctors[:3]):  # Create shifts for first 3 doctors
            for day_offset in range(7):  # Next 7 days
                shift_date = datetime.now().date() + timedelta(days=day_offset)
                
                # Create morning shift
                morning_shift = Shift(
                    doctor_id=doctor.id,
                    date=shift_date,
                    start_time=datetime.strptime('09:00', '%H:%M').time(),
                    end_time=datetime.strptime('13:00', '%H:%M').time(),
                    shift_type='morning',
                    consultation_mode=doctor.consultation_mode,
                    max_patients=8,
                    is_active=True
                )
                db.session.add(morning_shift)
                db.session.commit()  # Commit to get the shift ID
                
                # Create slots for morning shift
                for slot_num in range(8):
                    slot_time = datetime.strptime('09:00', '%H:%M') + timedelta(minutes=15 * slot_num)
                    slot = Slot(
                        shift_id=morning_shift.id,
                        token_number=slot_num + 1,
                        start_time=slot_time.time(),
                        end_time=(slot_time + timedelta(minutes=15)).time(),
                        duration_minutes=15,
                        is_booked=False,
                        is_locked=False
                    )
                    db.session.add(slot)
                
                db.session.commit()  # Commit all slots for this shift
        
        print("Database initialized successfully!")
        print("\nLogin Credentials:")
        print("Admin: admin@hospital.com / admin123")
        print("Doctors:")
        for doctor in doctors:
            print(f"  {doctor.full_name}: {doctor.user.email} / {doctor.user.email.replace('dr.', '').split('@')[0]}123")
        print("Patients:")
        for patient in Patient.query.all():
            print(f"  {patient.full_name}: {patient.user.email} / patient123")

if __name__ == '__main__':
    try:
        init_database()
        print("\n✅ Database initialization completed successfully!")
    except Exception as e:
        print(f"\n❌ Error initializing database: {e}")
        sys.exit(1)
