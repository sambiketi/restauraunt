from flask import Blueprint, request, jsonify
from models import Reservation
from flask_login import login_required, current_user
from db_postgres import db
from datetime import datetime

reservation_bp = Blueprint('reservations', __name__)

@reservation_bp.route('/', methods=['GET'])
def get_public_reservations():
    return jsonify({'message': 'Public reservation endpoint'})

@reservation_bp.route('/availability', methods=['GET'])
def check_availability():
    date = request.args.get('date')
    time = request.args.get('time')
    guests = int(request.args.get('guests', 2))
    
    # Get all reservations for that date using SQLAlchemy
    reservations = Reservation.query.filter_by(reservation_date=date).all()
    total_reserved = sum(r.number_of_guests for r in reservations)
    
    # Assuming max capacity of 50 guests per session
    available = total_reserved + guests <= 50
    
    return jsonify({
        'available': available,
        'total_reserved': total_reserved,
        'requested_guests': guests,
        'date': date,
        'time': time
    })
