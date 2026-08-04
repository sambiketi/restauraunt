from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from models import Order, MenuItem, Customer, EmailSubscriber, Reservation, Table, Coupon
from db_postgres import db
from datetime import datetime

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/stats', methods=['GET'])
@login_required
def get_stats():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    orders = Order.query.all()
    total_orders = len(orders)
    
    # Today's revenue
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(db.func.date(Order.created_at) == today).all()
    today_revenue = sum(o.total for o in today_orders)
    
    total_menu = MenuItem.query.count()
    total_customers = Customer.query.count()
    
    return jsonify({
        'total_orders': total_orders,
        'today_revenue': round(today_revenue, 2),
        'total_menu': total_menu,
        'total_customers': total_customers
    })

@admin_bp.route('/orders', methods=['GET'])
@login_required
def get_all_orders():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    orders = Order.query.order_by(Order.created_at.desc()).all()
    return jsonify([order.to_dict() for order in orders])

@admin_bp.route('/customers', methods=['GET'])
@login_required
def get_all_customers():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    customers = Customer.query.all()
    return jsonify([customer.to_dict() for customer in customers])

@admin_bp.route('/email-subscribers', methods=['GET'])
@login_required
def get_email_subscribers():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    subscribers = EmailSubscriber.query.all()
    return jsonify([sub.to_dict() for sub in subscribers])

@admin_bp.route('/email-subscribers', methods=['POST'])
@login_required
def add_email_subscriber():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    email = data.get('email')
    name = data.get('name')
    source = data.get('source', 'admin')
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    # Check if subscriber already exists
    existing = EmailSubscriber.query.filter_by(email=email).first()
    if existing:
        return jsonify({'error': 'Email already subscribed'}), 400
    
    subscriber = EmailSubscriber(
        email=email,
        name=name,
        source=source,
        is_active=True
    )
    db.session.add(subscriber)
    db.session.commit()
    
    return jsonify(subscriber.to_dict()), 201

@admin_bp.route('/email-subscribers/<int:subscriber_id>', methods=['DELETE'])
@login_required
def delete_email_subscriber(subscriber_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    subscriber = EmailSubscriber.query.get(subscriber_id)
    if not subscriber:
        return jsonify({'error': 'Subscriber not found'}), 404
    
    subscriber.is_active = False
    subscriber.unsubscribed_at = datetime.utcnow()
    db.session.commit()
    
    return jsonify({'message': 'Subscriber removed successfully'})

@admin_bp.route('/reservations', methods=['GET'])
@login_required
def get_all_reservations():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    reservations = Reservation.query.all()
    return jsonify([r.to_dict() for r in reservations])

@admin_bp.route('/reservations', methods=['POST'])
@login_required
def create_reservation():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    required = ['guest_name', 'guest_email', 'guest_phone', 'reservation_date', 'reservation_time', 'number_of_guests']
    
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    reservation = Reservation(
        guest_name=data['guest_name'],
        guest_email=data['guest_email'],
        guest_phone=data['guest_phone'],
        reservation_date=data['reservation_date'],
        reservation_time=data['reservation_time'],
        number_of_guests=data['number_of_guests'],
        table_number=data.get('table_number'),
        special_requests=data.get('special_requests'),
        source=data.get('source', 'website')
    )
    db.session.add(reservation)
    db.session.commit()
    
    return jsonify(reservation.to_dict()), 201

@admin_bp.route('/reservations/<int:reservation_id>/status', methods=['PUT'])
@login_required
def update_reservation_status(reservation_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    reservation = Reservation.query.get(reservation_id)
    if not reservation:
        return jsonify({'error': 'Reservation not found'}), 404
    
    data = request.json
    status = data.get('status')
    
    if not status:
        return jsonify({'error': 'Status is required'}), 400
    
    reservation.status = status
    
    if status == 'confirmed':
        reservation.confirmed_at = datetime.utcnow()
    elif status == 'seated':
        reservation.seated_at = datetime.utcnow()
    elif status == 'completed':
        reservation.completed_at = datetime.utcnow()
    elif status == 'cancelled':
        reservation.cancelled_at = datetime.utcnow()
        reservation.cancelled_reason = data.get('reason')
    
    db.session.commit()
    return jsonify(reservation.to_dict())

@admin_bp.route('/tables', methods=['GET'])
@login_required
def get_all_tables():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    tables = Table.query.all()
    return jsonify([t.to_dict() for t in tables])

@admin_bp.route('/coupons', methods=['GET'])
@login_required
def get_all_coupons():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    coupons = Coupon.query.all()
    return jsonify([c.to_dict() for c in coupons])

@admin_bp.route('/coupons', methods=['POST'])
@login_required
def create_coupon():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    required = ['code', 'discount_type', 'discount_value', 'start_date', 'end_date']
    
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Check if coupon code already exists
    existing = Coupon.query.filter_by(code=data['code']).first()
    if existing:
        return jsonify({'error': 'Coupon code already exists'}), 400
    
    coupon = Coupon(
        code=data['code'],
        description=data.get('description', ''),
        discount_type=data['discount_type'],
        discount_value=data['discount_value'],
        minimum_order=data.get('minimum_order', 0),
        max_uses=data.get('max_uses'),
        start_date=data['start_date'],
        end_date=data['end_date'],
        is_active=data.get('is_active', True)
    )
    db.session.add(coupon)
    db.session.commit()
    
    return jsonify(coupon.to_dict()), 201

@admin_bp.route('/coupons/<int:coupon_id>', methods=['DELETE'])
@login_required
def delete_coupon(coupon_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    coupon = Coupon.query.get(coupon_id)
    if not coupon:
        return jsonify({'error': 'Coupon not found'}), 404
    
    db.session.delete(coupon)
    db.session.commit()
    
    return jsonify({'message': 'Coupon deleted successfully'})

@admin_bp.route('/dashboard/summary', methods=['GET'])
@login_required
def get_dashboard_summary():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Get all orders
    orders = Order.query.all()
    total_orders = len(orders)
    
    # Calculate revenue by status
    revenue_by_status = {}
    for order in orders:
        status = order.status
        if status not in revenue_by_status:
            revenue_by_status[status] = 0
        revenue_by_status[status] += order.total
    
    # Get today's date
    today = datetime.utcnow().date()
    today_orders = Order.query.filter(db.func.date(Order.created_at) == today).all()
    
    # Get recent orders (last 10)
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # Get menu stats
    menu_items = MenuItem.query.all()
    available_items = [i for i in menu_items if i.is_available]
    featured_items = [i for i in menu_items if i.featured]
    
    # Get customer stats
    customers = Customer.query.all()
    
    # Get reservation stats
    reservations = Reservation.query.all()
    pending_reservations = [r for r in reservations if r.status == 'pending']
    
    return jsonify({
        'total_orders': total_orders,
        'today_orders': len(today_orders),
        'today_revenue': round(sum(o.total for o in today_orders), 2),
        'total_revenue': round(sum(o.total for o in orders), 2),
        'revenue_by_status': revenue_by_status,
        'total_menu_items': len(menu_items),
        'available_menu_items': len(available_items),
        'featured_menu_items': len(featured_items),
        'total_customers': len(customers),
        'total_reservations': len(reservations),
        'pending_reservations': len(pending_reservations),
        'recent_orders': [o.to_dict() for o in recent_orders]
    })
