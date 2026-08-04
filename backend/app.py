import os
from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from models import User
from routes import register_blueprints
from config import config
from db_postgres import db, init_db

bcrypt = Bcrypt()
login_manager = LoginManager()

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='static')
    app.config.from_object(config[config_name])
    
    # Initialize database
    init_db(app)
    
    bcrypt.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    CORS(app, origins=app.config['CORS_ORIGINS'])
    register_blueprints(app)

    @app.route('/')
    def index():
        return send_from_directory('static', 'index.html')

    @app.route('/<path:path>')
    def serve_static(path):
        return send_from_directory('static', path)

    # Create tables
    with app.app_context():
        db.create_all()
        print('✅ Database tables created!')

    return app

if __name__ == '__main__':
    app = create_app('development')
    app.run(debug=True, host='0.0.0.0', port=5000)
