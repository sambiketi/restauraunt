from flask import Blueprint, request, jsonify
from models import Order, Customer
from flask_login import login_required, current_user
from db_postgres import db
import json
import random
from datetime import datetime

order_bp = Blueprint('orders', __name__)

@order_bp.route('/', methods=['POST'])
def create_order():
    data = request.json
    
    # Validate required fields
    required = ['customer', 'items']
    for field in required:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Calculate totals
    subtotal = sum(item['price'] * item['quantity'] for item in data['items'])
    delivery_fee = 0 if subtotal > 30 or data['customer'].get('delivery_method') == 'pickup' else 5.99
    tax = subtotal * 0.085
    total = subtotal + delivery_fee + tax
    
    # Generate order number
    order_number = f'RT{random.randint(100000, 999999)}'
    
    # Create order
    order = Order(
        order_number=order_number,
        customer_name=data['customer']['name'],
        customer_phone=data['customer']['phone'],
        customer_email=data['customer']['email'],
        customer_address=data['customer']['address'],
        customer_city=data['customer']['city'],
        customer_postal=data['customer']['postal'],
        delivery_instructions=data['customer'].get('instructions', ''),
        customer_type=data['customer']['type'],
        delivery_method=data['customer']['delivery_method'],
        payment_method=data['customer']['payment_method'],
        items=json.dumps(data['items']),
        subtotal=subtotal,
        delivery_fee=delivery_fee,
        tax=tax,
        total=total,
        estimated_time='30-45 Minutes',
        order_source=data.get('source', 'website'),
        special_requests=data.get('special_requests', '')
    )
    db.session.add(order)
    db.session.commit()
    
    # Create/update customer
    email = data['customer']['email']
    customer = Customer.query.filter_by(email=email).first()
    
    if customer:
        customer.total_orders += 1
        customer.total_spent += total
        customer.last_order_date = datetime.utcnow()
    else:
        customer = Customer(
            name=data['customer']['name'],
            email=email,
            phone=data['customer']['phone'],
            address=data['customer']['address'],
            city=data['customer']['city'],
            postal=data['customer']['postal'],
            total_orders=1,
            total_spent=total,
            last_order_date=datetime.utcnow()
        )
        db.session.add(customer)
    
    db.session.commit()
    
    return jsonify(order.to_dict()), 201

@order_bp.route('/<string:order_number>', methods=['GET'])
def get_order(order_number):
    order = Order.query.filter_by(order_number=order_number).first()
    if order:
        return jsonify(order.to_dict())
    return jsonify({'error': 'Order not found'}), 404

@order_bp.route('/', methods=['GET'])
@login_required
def get_orders():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    status = request.args.get('status')
    if status:
        orders = Order.query.filter_by(status=status).all()
    else:
        orders = Order.query.order_by(Order.created_at.desc()).all()
    
    return jsonify([order.to_dict() for order in orders])

@order_bp.route('/<string:order_number>/status', methods=['PUT'])
@login_required
def update_order_status(order_number):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    order = Order.query.filter_by(order_number=order_number).first()
    if not order:
        return jsonify({'error': 'Order not found'}), 404
    
    data = request.json
    status = data.get('status')
    if not status:
        return jsonify({'error': 'Status required'}), 400
    
    order.status = status
    if status == 'cancelled':
        order.cancelled_at = datetime.utcnow()
        order.cancelled_reason = data.get('reason')
    
    db.session.commit()
    return jsonify(order.to_dict())
