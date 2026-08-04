from datetime import datetime
from flask_login import UserMixin
from db_postgres import db
import json

# ========================================
# USER MODEL
# ========================================
class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(200), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'is_admin': self.is_admin,
            'is_active': self.is_active,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# ========================================
# MENU ITEM MODEL
# ========================================
class MenuItem(db.Model):
    __tablename__ = 'menu_items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50), nullable=False)
    price = db.Column(db.Float, nullable=False)
    description = db.Column(db.Text, nullable=False)
    calories = db.Column(db.Integer, nullable=False)
    prep_time = db.Column(db.String(20), nullable=False)
    rating = db.Column(db.Float, default=4.5)
    image = db.Column(db.String(200), nullable=False)
    is_available = db.Column(db.Boolean, default=True)
    featured = db.Column(db.Boolean, default=False)
    is_vegetarian = db.Column(db.Boolean, default=False)
    is_vegan = db.Column(db.Boolean, default=False)
    is_gluten_free = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<MenuItem {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'category': self.category,
            'price': float(self.price),
            'description': self.description,
            'calories': self.calories,
            'prep_time': self.prep_time,
            'rating': float(self.rating) if self.rating else 4.5,
            'image': self.image,
            'is_available': self.is_available,
            'featured': self.featured,
            'is_vegetarian': self.is_vegetarian,
            'is_vegan': self.is_vegan,
            'is_gluten_free': self.is_gluten_free
        }

# ========================================
# ORDER MODEL
# ========================================
class Order(db.Model):
    __tablename__ = 'orders'

    id = db.Column(db.Integer, primary_key=True)
    order_number = db.Column(db.String(20), unique=True, nullable=False)
    customer_name = db.Column(db.String(100), nullable=False)
    customer_phone = db.Column(db.String(20), nullable=False)
    customer_email = db.Column(db.String(120), nullable=False)
    customer_address = db.Column(db.Text, nullable=False)
    customer_city = db.Column(db.String(50), nullable=False)
    customer_postal = db.Column(db.String(20), nullable=False)
    delivery_instructions = db.Column(db.Text)
    customer_type = db.Column(db.String(20), default='new')
    delivery_method = db.Column(db.String(20), default='delivery')
    payment_method = db.Column(db.String(20), default='credit')
    status = db.Column(db.String(20), default='preparing')
    items = db.Column(db.Text, nullable=False)  # JSON string
    subtotal = db.Column(db.Float, nullable=False)
    delivery_fee = db.Column(db.Float, default=0)
    tax = db.Column(db.Float, default=0)
    total = db.Column(db.Float, nullable=False)
    estimated_time = db.Column(db.String(50), default='30-45 Minutes')
    order_source = db.Column(db.String(20), default='website')
    special_requests = db.Column(db.Text)
    cancelled_at = db.Column(db.DateTime)
    cancelled_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Order {self.order_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'order_number': self.order_number,
            'customer_name': self.customer_name,
            'customer_phone': self.customer_phone,
            'customer_email': self.customer_email,
            'customer_address': self.customer_address,
            'customer_city': self.customer_city,
            'customer_postal': self.customer_postal,
            'delivery_instructions': self.delivery_instructions,
            'customer_type': self.customer_type,
            'delivery_method': self.delivery_method,
            'payment_method': self.payment_method,
            'status': self.status,
            'items': json.loads(self.items) if self.items else [],
            'subtotal': float(self.subtotal),
            'delivery_fee': float(self.delivery_fee),
            'tax': float(self.tax),
            'total': float(self.total),
            'estimated_time': self.estimated_time,
            'order_source': self.order_source,
            'special_requests': self.special_requests,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ========================================
# RESERVATION MODEL
# ========================================
class Reservation(db.Model):
    __tablename__ = 'reservations'

    id = db.Column(db.Integer, primary_key=True)
    guest_name = db.Column(db.String(100), nullable=False)
    guest_email = db.Column(db.String(120), nullable=False)
    guest_phone = db.Column(db.String(20), nullable=False)
    reservation_date = db.Column(db.Date, nullable=False)
    reservation_time = db.Column(db.Time, nullable=False)
    number_of_guests = db.Column(db.Integer, nullable=False)
    table_number = db.Column(db.Integer)
    special_requests = db.Column(db.Text)
    status = db.Column(db.String(20), default='pending')
    source = db.Column(db.String(20), default='website')
    confirmed_at = db.Column(db.DateTime)
    seated_at = db.Column(db.DateTime)
    completed_at = db.Column(db.DateTime)
    cancelled_at = db.Column(db.DateTime)
    cancelled_reason = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Reservation {self.id} - {self.guest_name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'guest_name': self.guest_name,
            'guest_email': self.guest_email,
            'guest_phone': self.guest_phone,
            'reservation_date': self.reservation_date.isoformat() if self.reservation_date else None,
            'reservation_time': self.reservation_time.isoformat() if self.reservation_time else None,
            'number_of_guests': self.number_of_guests,
            'table_number': self.table_number,
            'special_requests': self.special_requests,
            'status': self.status,
            'source': self.source,
            'confirmed_at': self.confirmed_at.isoformat() if self.confirmed_at else None,
            'seated_at': self.seated_at.isoformat() if self.seated_at else None,
            'completed_at': self.completed_at.isoformat() if self.completed_at else None,
            'cancelled_at': self.cancelled_at.isoformat() if self.cancelled_at else None,
            'cancelled_reason': self.cancelled_reason,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ========================================
# CUSTOMER MODEL
# ========================================
class Customer(db.Model):
    __tablename__ = 'customers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    address = db.Column(db.Text)
    city = db.Column(db.String(50))
    postal = db.Column(db.String(20))
    total_orders = db.Column(db.Integer, default=0)
    total_spent = db.Column(db.Float, default=0)
    last_order_date = db.Column(db.DateTime)
    joined_date = db.Column(db.DateTime, default=datetime.utcnow)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Customer {self.name}>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'phone': self.phone,
            'address': self.address,
            'city': self.city,
            'postal': self.postal,
            'total_orders': self.total_orders,
            'total_spent': float(self.total_spent),
            'last_order_date': self.last_order_date.isoformat() if self.last_order_date else None,
            'joined_date': self.joined_date.isoformat() if self.joined_date else None,
            'notes': self.notes
        }

# ========================================
# EMAIL SUBSCRIBER MODEL
# ========================================
class EmailSubscriber(db.Model):
    __tablename__ = 'email_subscribers'

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    name = db.Column(db.String(100))
    is_active = db.Column(db.Boolean, default=True)
    source = db.Column(db.String(50), default='website')
    unsubscribed_at = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<EmailSubscriber {self.email}>'

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'name': self.name,
            'is_active': self.is_active,
            'source': self.source,
            'unsubscribed_at': self.unsubscribed_at.isoformat() if self.unsubscribed_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

# ========================================
# TABLE MODEL (Restaurant Tables)
# ========================================
class Table(db.Model):
    __tablename__ = 'tables'

    id = db.Column(db.Integer, primary_key=True)
    table_number = db.Column(db.Integer, unique=True, nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    section = db.Column(db.String(50))
    is_available = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Table {self.table_number}>'

    def to_dict(self):
        return {
            'id': self.id,
            'table_number': self.table_number,
            'capacity': self.capacity,
            'section': self.section,
            'is_available': self.is_available
        }

# ========================================
# COUPON MODEL
# ========================================
class Coupon(db.Model):
    __tablename__ = 'coupons'

    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(50), unique=True, nullable=False)
    description = db.Column(db.Text)
    discount_type = db.Column(db.String(20), nullable=False)  # percentage, fixed
    discount_value = db.Column(db.Float, nullable=False)
    minimum_order = db.Column(db.Float, default=0)
    max_uses = db.Column(db.Integer)
    used_count = db.Column(db.Integer, default=0)
    start_date = db.Column(db.DateTime, nullable=False)
    end_date = db.Column(db.DateTime, nullable=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<Coupon {self.code}>'

    def to_dict(self):
        return {
            'id': self.id,
            'code': self.code,
            'description': self.description,
            'discount_type': self.discount_type,
            'discount_value': float(self.discount_value),
            'minimum_order': float(self.minimum_order),
            'max_uses': self.max_uses,
            'used_count': self.used_count,
            'start_date': self.start_date.isoformat() if self.start_date else None,
            'end_date': self.end_date.isoformat() if self.end_date else None,
            'is_active': self.is_active
        }
