# Doctor Appointment System

![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)
![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.0+-purple.svg)
![SQLite](https://img.shields.io/badge/SQLite-3.0+-red.svg)
![License](https://img.shields.io/badge/License-MIT-yellow.svg)

A comprehensive hospital appointment management system supporting Admin, Doctor, and Patient workflows with strict Online/Offline mode separation.

## 📋 Features

### Admin Role

- **Dashboard Overview**: Total appointments, revenue statistics, doctor/patient counts
- **Doctor Management**: Add/update/deactivate doctors with specialities and consultation modes
- **Shift Management**: Create and manage doctor shifts (Morning/Evening/Night)
- **Slot & Token Management**: Generate time-based slots with token numbers
- **System Monitoring**: Track appointment lifecycle and generate reports

### Doctor Role

- **Schedule Access**: View assigned duty schedules (read-only)
- **Appointment Handling**: Update appointment status (confirmed/completed/cancelled/no-show)
- **Prescription Management**: Add diagnosis, medicines, and follow-up instructions
- **Online Consultation**: Add secure video consultation links
- **Offline Consultation**: Display clinic address automatically

### Patient Role

- **Dashboard**: Toggle between Online/Offline mode, view appointments
- **Doctor Filtering**: Filter by speciality, availability, and consultation mode
- **Appointment Booking**: Select available shifts and slots, receive token numbers
- **Medical History**: View past prescriptions and consultation notes
- **Online/Offline Appointments**: Access video links or clinic information

## 🛠️ Tech Stack

### Backend

- **Python 3.8+**
- **Flask** - Web framework
- **Flask-SQLAlchemy** - ORM
- **Flask-Login** - Authentication
- **Flask-Migrate** - Database migrations
- **Flask-WTF** - Form handling
- **Flask-Bcrypt** - Password hashing
- **Flask-SocketIO** - Real-time support
- **SQLite** - Database (Development)
- **PostgreSQL** - Database (Production - optional)

### Frontend

- **HTML5**
- **CSS3**
- **Bootstrap 5**
- **JavaScript**
- **Jinja2 Templates**

### Realtime & Video

- **WebRTC or Jitsi Meet** (planned)
- **Flask-SocketIO**

### Charts & Analytics

- **Chart.js**

## 🚀 Installation

### Prerequisites

- Python 3.8+
- pip and virtualenv

### Quick Start

1. **Clone and setup**

   ```bash
   git clone <repository-url>
   cd doctor-appointment-system
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # macOS/Linux
   source venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Start application** (auto-checks database)

   ```bash
   python start.py
   ```

4. **Access the application**
   - Open browser: `http://localhost:5000`
   - Admin: <admin@hospital.com> / admin123
   - Patient: <patient1@email.com> / patient123

### Database Setup

#### SQLite (Default - Development)

- Database: `instance/doctor_appointment_dev.db`
- Auto-initialized on first run
- Sample data included

#### Manual Database Management

```bash
# Check database status
python check_database.py

# Initialize/reset database
python init_sqlite.py
```

### Project Structure

```text
doctor-appointment-system/
├── 📄 .env                    # Environment variables
├── 📄 README.md               # Project documentation
├── 📄 requirements.txt         # Python dependencies
├── 📄 config.py               # Configuration settings
├── 📄 run.py                  # Main application entry point
├── 📄 start.py                # Enhanced startup script
├── 📄 check_database.py       # Database status checker
├── 📄 init_sqlite.py         # Database initializer
├── 📁 app/                    # Main application code
│   ├── 📁 models/             # Database models
│   ├── 📁 routes/             # Application routes
│   ├── 📁 static/             # CSS, JS, assets
│   └── 📁 templates/          # HTML templates
├── 📁 instance/               # Database file
└── 📁 venv/                   # Virtual environment
```

*See `PROJECT_STRUCTURE.md` for detailed structure.*

## 🔐 Default Login Credentials

### Admin

- Email: `admin@hospital.com`
- Password: `admin123`

### Doctors

- Dr. John Smith: `dr.smith@hospital.com` / `smith123`
- Dr. Sarah Johnson: `dr.johnson@hospital.com` / `johnson123`
- Dr. Michael Wilson: `dr.wilson@hospital.com` / `wilson123`
- Dr. Emily Brown: `dr.brown@hospital.com` / `brown123`
- Dr. Robert Davis: `dr.davis@hospital.com` / `davis123`

### Patients

- Alice Johnson: `patient1@email.com` / `patient123`
- Bob Smith: `patient2@email.com` / `patient123`
- Carol Williams: `patient3@email.com` / `patient123`

## Features

### 🎯 Key Features

- **Role-based Access**: Admin, Doctor, Patient workflows
- **Online/Offline Modes**: Separate consultation modes
- **Token-based Booking**: Unique appointment tokens
- **Shift Management**: Morning/Evening/Night shifts
- **Prescription System**: Complete medical prescriptions
- **Enhanced UI/UX**: Modern login/register pages
- **SQLite Database**: Ready-to-use with sample data

### 🛠️ Technical Features

- **Flask Framework**: Modern web framework
- **SQLAlchemy ORM**: Database management
- **Flask-Login**: Authentication system
- **Bootstrap 5**: Responsive UI components
- **Jinja2 Templates**: Server-side rendering
- **Real-time Support**: Flask-SocketIO ready

## Development

### Adding New Features

1. Create models in `app/models/`
2. Add routes in `app/routes/`
3. Create templates in `app/templates/`
4. Update static files in `app/static/`

### Database Changes

```bash
# Reset database with new schema
python init_sqlite.py
```

### Configuration

- Environment variables in `.env`
- Database settings in `config.py`
- Application factory in `app/__init__.py`

## License

This project is for educational and demonstration purposes.

## Support

For issues and questions, please refer to the project documentation.

## 📁 Detailed Project Structure

```text

## Database Schema

The system uses the following main entities:

- **Users**: Base user authentication with role-based access
- **Admins**: Hospital administrators
- **Doctors**: Medical practitioners with specialities
- **Patients**: Individuals seeking medical consultations
- **Specialities**: Medical specializations
- **Shifts**: Doctor duty schedules
- **Slots**: Time-based appointment slots with tokens
- **Appointments**: Patient-doctor consultations
- **Prescriptions**: Medical prescriptions with medicines
- **Medicines**: Available medications database

## ⚙️ Advanced Development

### Environment Variables

Create a `.env` file in the root directory:

```bash
FLASK_APP=run.py
FLASK_ENV=development
SECRET_KEY=your-secret-key-here
DATABASE_URL=postgresql://username:password@localhost/doctor_appointment
```

### Database Migrations

```bash
# Initialize migration
flask db init

# Create migration
flask db migrate -m "Initial migration"

# Apply migration
flask db upgrade
```

### Testing

```bash
# Run tests
python -m pytest

# Run with coverage
python -m pytest --cov=app
```

## 📄 License

This project is licensed under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📞 Support

For support and questions, please open an issue in the repository or contact:
**Madhan Mohan Reddy**

- 📧 Email: [madhanmohanreddyperam06@gmail.com](mailto:madhanmohanreddyperam06@gmail.com)
- 📱 Mobile: +91 9110395993
