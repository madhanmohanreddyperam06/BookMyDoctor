#!/usr/bin/env python3
"""
Simple startup script for Doctor Appointment System
"""

import os
import sys
import subprocess
import time

def check_database():
    """Check if database is properly initialized"""
    try:
        from app import create_app, db
        from app.models import User, Doctor, Patient, Admin
        
        app = create_app()
        with app.app_context():
            user_count = User.query.count()
            if user_count == 0:
                print("❌ Database not initialized!")
                print("🔧 Please run: python init_sqlite.py")
                return False
            else:
                print(f"✅ Database ready with {user_count} users")
                return True
    except Exception as e:
        print(f"❌ Database error: {e}")
        return False

def start_app():
    """Start the Flask application"""
    print("🚀 Starting Doctor Appointment System...")
    
    # Check database first
    if not check_database():
        return
    
    print("🌐 Starting web server...")
    print("📍 Access the application at: http://localhost:5000")
    print("🔑 Login credentials:")
    print("   Admin: admin@hospital.com / admin123")
    print("   Patient: patient1@email.com / patient123")
    print("\n⏹️  Press Ctrl+C to stop the server")
    print("-" * 50)
    
    try:
        from app import create_app, socketio
        app = create_app()
        socketio.run(app, debug=True, host='0.0.0.0', port=5000)
    except KeyboardInterrupt:
        print("\n⏹️  Server stopped by user")
    except Exception as e:
        print(f"❌ Error starting server: {e}")

if __name__ == '__main__':
    start_app()
