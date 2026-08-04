from flask import Blueprint
from .menu_routes import menu_bp
from .order_routes import order_bp
from .auth_routes import auth_bp
from .admin_routes import admin_bp
from .reservation_routes import reservation_bp

def register_blueprints(app):
    app.register_blueprint(menu_bp, url_prefix='/api/menu')
    app.register_blueprint(order_bp, url_prefix='/api/orders')
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(reservation_bp, url_prefix='/api/reservations')
