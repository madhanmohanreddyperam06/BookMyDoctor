#!/usr/bin/env python3
"""
Check database status and initialize if needed
"""

import os
import sys

# Add project root to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User, Admin, Doctor, Patient, Speciality, Medicine

def check_database():
    """Check database status"""
    app = create_app()
    
    with app.app_context():
        try:
            # Check if tables exist
            inspector = db.inspect(db.engine)
            tables = inspector.get_table_names()
            
            print("📊 Database Status Check")
            print("=" * 50)
            print(f"Database: {db.engine.url}")
            print(f"Tables found: {len(tables)}")
            
            # Check if data exists
            if 'users' in tables:
                user_count = User.query.count()
                print(f"Users: {user_count}")
                
                if user_count == 0:
                    print("❌ No data found in database")
                    print("\n🔧 To initialize database, run:")
                    print("   python init_sqlite.py")
                    return False
                else:
                    admin_count = Admin.query.count()
                    doctor_count = Doctor.query.count()
                    patient_count = Patient.query.count()
                    
                    print(f"Admins: {admin_count}")
                    print(f"Doctors: {doctor_count}")
                    print(f"Patients: {patient_count}")
                    
                    if 'specialities' in tables:
                        speciality_count = Speciality.query.count()
                        print(f"Specialities: {speciality_count}")
                    
                    if 'medicines' in tables:
                        medicine_count = Medicine.query.count()
                        print(f"Medicines: {medicine_count}")
                    
                    print("\n✅ Database is properly initialized!")
                    return True
            else:
                print("❌ No tables found")
                print("\n🔧 To initialize database, run:")
                print("   python init_sqlite.py")
                return False
                
        except Exception as e:
            print(f"❌ Error checking database: {e}")
            return False

if __name__ == '__main__':
    check_database()
