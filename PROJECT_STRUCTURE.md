# Doctor Appointment System - Project Structure

## 📁 Clean Project Structure

```
e:\Doctor Appointment System\
├── 📄 .env                    # Environment variables
├── 📄 README.md               # Project documentation
├── 📄 requirements.txt         # Python dependencies
├── 📄 config.py               # Configuration settings
├── 📄 run.py                  # Main application entry point
├── 📄 start.py                # Enhanced startup script
├── 📄 check_database.py       # Database status checker
├── 📄 init_sqlite.py         # Database initializer
├── 📄 PROJECT_STRUCTURE.md    # This file
├── 📁 app/                    # Main application code
│   ├── 📄 __init__.py         # App factory and extensions
│   ├── 📁 models/             # Database models
│   │   ├── 📄 user.py         # User model
│   │   ├── 📄 admin.py        # Admin model
│   │   ├── 📄 doctor.py       # Doctor model
│   │   ├── 📄 patient.py      # Patient model
│   │   ├── 📄 speciality.py   # Speciality model
│   │   ├── 📄 shift.py        # Shift model
│   │   ├── 📄 slot.py         # Slot model
│   │   ├── 📄 appointment.py  # Appointment model
│   │   ├── 📄 prescription.py # Prescription model
│   │   ├── 📄 medicine.py     # Medicine model
│   │   └── 📄 __init__.py     # Model imports
│   ├── 📁 routes/             # Application routes
│   │   ├── 📄 auth.py         # Authentication routes
│   │   ├── 📄 admin.py        # Admin routes
│   │   ├── 📄 doctor.py       # Doctor routes
│   │   ├── 📄 patient.py      # Patient routes
│   │   ├── 📄 main.py         # Main routes
│   │   └── 📄 video.py        # Video consultation routes
│   ├── 📁 static/             # Static files
│   │   ├── 📁 css/            # Stylesheets
│   │   │   └── 📄 style.css   # Main styles
│   │   └── 📁 js/             # JavaScript files
│   └── 📁 templates/          # HTML templates
│       ├── 📁 auth/           # Authentication templates
│       ├── 📁 admin/          # Admin templates
│       ├── 📁 doctor/         # Doctor templates
│       ├── 📁 patient/        # Patient templates
│       └── 📄 base.html       # Base template
├── 📁 instance/               # Instance-specific files
│   └── 📄 doctor_appointment_dev.db  # SQLite database
└── 📁 venv/                   # Virtual environment
```

## 🗑️ Removed Files

The following unnecessary files were removed to keep the project clean:

- ❌ `init_db.py` - Duplicate database initialization (replaced by `init_sqlite.py`)
- ❌ `test_system.py` - Test script (not needed for production)
- ❌ `migrations/` - Empty directory (not using Flask-Migrate)
- ❌ `__pycache__/` - Python cache files (auto-generated)

## 🎯 Essential Files

### **Core Application**
- `run.py` - Main application entry point
- `start.py` - Enhanced startup with database check
- `config.py` - Configuration management
- `.env` - Environment variables

### **Database**
- `init_sqlite.py` - Database initialization with sample data
- `check_database.py` - Database status and health check
- `instance/doctor_appointment_dev.db` - SQLite database file

### **Documentation**
- `README.md` - Complete project documentation
- `requirements.txt` - Python dependencies
- `PROJECT_STRUCTURE.md` - Project structure reference

### **Application Code**
- `app/` - Complete application source code
  - `models/` - Database models
  - `routes/` - Flask blueprints and routes
  - `static/` - CSS, JS, and assets
  - `templates/` - Jinja2 templates

## 🚀 Usage

### **Start Application**
```bash
# Option 1: Direct start
python run.py

# Option 2: Enhanced start (recommended)
python start.py
```

### **Database Management**
```bash
# Check database status
python check_database.py

# Initialize/reset database
python init_sqlite.py
```

### **Access**
- **URL**: http://localhost:5000
- **Admin**: admin@hospital.com / admin123
- **Patient**: patient1@email.com / patient123

## 📋 Features

- ✅ **Clean Structure**: Only essential files included
- ✅ **SQLite Database**: Ready-to-use database with sample data
- ✅ **Enhanced UI**: Modern login/register pages
- ✅ **Role-based Access**: Admin, Doctor, Patient roles
- ✅ **Complete Documentation**: README and structure guide
- ✅ **Easy Setup**: One-command startup with database check

## 🎉 Benefits

- **Clean Codebase**: No unnecessary files
- **Easy Maintenance**: Clear structure and documentation
- **Quick Setup**: Ready to run in minutes
- **Production Ready**: Proper configuration and structure
