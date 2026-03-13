from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_socketio import SocketIO
from config import config

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
migrate = Migrate()
bcrypt = Bcrypt()
socketio = SocketIO()

def create_app(config_name='default'):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions with app
    db.init_app(app)
    login_manager.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)
    socketio.init_app(app)
    
    # Configure login manager
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'
    
    # User loader function
    @login_manager.user_loader
    def load_user(user_id):
        from app.models.user import User
        return User.query.get(int(user_id))
    
    # Make timedelta available in templates
    from datetime import timedelta
    app.jinja_env.globals['timedelta'] = timedelta
    
    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from app.routes.admin import admin as admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')
    
    from app.routes.doctor import doctor as doctor_blueprint
    app.register_blueprint(doctor_blueprint, url_prefix='/doctor')
    
    from app.routes.patient import patient as patient_blueprint
    app.register_blueprint(patient_blueprint, url_prefix='/patient')
    
    from app.routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint)
    
    from app.routes.video import video as video_blueprint
    app.register_blueprint(video_blueprint, url_prefix='/video')
    
    return app
