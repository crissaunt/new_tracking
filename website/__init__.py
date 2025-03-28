import os
from flask import Flask
from flask_socketio import SocketIO
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from os import path

connected_users = {}
app = Flask(__name__)
socketio = SocketIO(app, cors_allowed_origins="*")

CORS(app, resources={r"/*": {"origins": "*"}})

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    
    app.config["SECRET_KEY"] =  os.environ.get('SECRET_KEY', 'fallback_secret_key')
    app.config["SQLALCHEMY_DATABASE_URI"] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    socketio = SocketIO(app, cors_allowed_origins="*")

    CORS(app, resources={r"/*": {"origins": "*"}})
    
    socketio.init_app(app, cors_allowed_origins="*")

    from .auth import auth
    app.register_blueprint(auth, url_prefix="/")
    
    from .views import views
    app.register_blueprint(views, url_prefix="/")
    
    
    create_database(app)
    from .models import User
    
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

def create_database(app):
    db_path = path.join(app.instance_path, DB_NAME)
    print(f"Database path: {db_path}")
    if not path.exists(db_path):
        print("Creating Database...")
        with app.app_context():
            db.create_all()
        print("Database is Created")
    else:
        print("Database is Already Created")        