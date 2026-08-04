from flask import Blueprint, request, jsonify
from models import MenuItem
from flask_login import login_required, current_user
from db_postgres import db

menu_bp = Blueprint('menu', __name__)

@menu_bp.route('/', methods=['GET'])
def get_menu():
    category = request.args.get('category')
    search = request.args.get('search')
    
    query = MenuItem.query.filter_by(is_available=True)
    
    if search:
        query = query.filter(
            db.or_(
                MenuItem.name.ilike(f'%{search}%'),
                MenuItem.description.ilike(f'%{search}%')
            )
        )
    elif category and category != 'all':
        query = query.filter_by(category=category)
    
    items = query.all()
    return jsonify([item.to_dict() for item in items])

@menu_bp.route('/featured', methods=['GET'])
def get_featured():
    items = MenuItem.query.filter_by(featured=True, is_available=True).limit(4).all()
    return jsonify([item.to_dict() for item in items])

@menu_bp.route('/<int:item_id>', methods=['GET'])
def get_menu_item(item_id):
    item = MenuItem.query.get(item_id)
    if item:
        return jsonify(item.to_dict())
    return jsonify({'error': 'Item not found'}), 404

@menu_bp.route('/', methods=['POST'])
@login_required
def create_menu_item():
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    data = request.json
    item = MenuItem(
        name=data['name'],
        category=data['category'],
        price=data['price'],
        description=data['description'],
        calories=data['calories'],
        prep_time=data['prep_time'],
        rating=data.get('rating', 4.5),
        image=data.get('image', 'images/pizza.jpg'),
        featured=data.get('featured', False),
        is_vegetarian=data.get('is_vegetarian', False),
        is_vegan=data.get('is_vegan', False),
        is_gluten_free=data.get('is_gluten_free', False)
    )
    db.session.add(item)
    db.session.commit()
    
    return jsonify(item.to_dict()), 201

@menu_bp.route('/<int:item_id>', methods=['PUT'])
@login_required
def update_menu_item(item_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    data = request.json
    for key, value in data.items():
        if hasattr(item, key):
            setattr(item, key, value)
    
    db.session.commit()
    return jsonify(item.to_dict())

@menu_bp.route('/<int:item_id>', methods=['DELETE'])
@login_required
def delete_menu_item(item_id):
    if not current_user.is_admin:
        return jsonify({'error': 'Unauthorized'}), 403
    
    item = MenuItem.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found'}), 404
    
    db.session.delete(item)
    db.session.commit()
    
    return jsonify({'message': 'Item deleted successfully'})
