from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import Config

# Initialize Flask extensions
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()

@login_manager.user_loader
def load_user(user_id):
    from app.models import User
    return User.query.get(int(user_id))

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions with app
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # Configure login manager
    login_manager.login_view = 'web_auth.login'
    login_manager.login_message = 'Please log in to access this page.'
    login_manager.login_message_category = 'info'

    # Add template context processor for current date
    @app.context_processor
    def inject_now():
        from datetime import datetime
        return {'now': datetime.utcnow()}

    # Register web route blueprints
    from app.routes.main import bp as main_bp
    from app.routes.auth import bp as auth_bp
    from app.routes.devices import bp as devices_bp
    from app.routes.sales import bp as sales_bp
    from app.routes.reports import bp as reports_bp
    
    app.register_blueprint(main_bp, name='main')
    app.register_blueprint(auth_bp, url_prefix='/auth', name='web_auth')
    app.register_blueprint(devices_bp, url_prefix='/devices', name='web_devices')
    app.register_blueprint(sales_bp, name='web_sales')
    app.register_blueprint(reports_bp, url_prefix='/reports', name='web_reports')
    
    # Register API blueprints
    from app.api.auth import bp as auth_api_bp
    from app.api.devices import bp as devices_api_bp
    from app.api.sales import bp as sales_api_bp
    from app.api.reports import bp as reports_api_bp
    
    app.register_blueprint(auth_api_bp, url_prefix='/api/auth', name='api_auth')
    app.register_blueprint(devices_api_bp, url_prefix='/api/devices', name='api_devices')
    app.register_blueprint(sales_api_bp, url_prefix='/api/sales', name='api_sales')
    app.register_blueprint(reports_api_bp, url_prefix='/api/reports', name='api_reports')

    return app