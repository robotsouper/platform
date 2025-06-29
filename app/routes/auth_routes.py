from flask import Blueprint, request, jsonify
from app import db
from app.models import User
from flask_jwt_extended import create_access_token
from datetime import timedelta
from werkzeug.security import generate_password_hash, check_password_hash


bp = Blueprint('auth_routes', __name__)

@bp.route('/register', methods=['POST'])
def register():
    data = request.json
    name = data.get('name')
    password = data.get('password')
    photo_url = data.get('photo_url')

    existing_user = User.query.filter_by(name=name).first()
    if existing_user:
        return jsonify({'error': 'Username already taken'}), 400
    
    hashed_password = generate_password_hash(password)
    new_user = User(name=name, password=hashed_password, photo_url=photo_url)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'User registered', 'user_id': new_user.user_id})


@bp.route('/login', methods=['POST'])   
def login():
    data = request.json
    name = data.get('name')
    password = data.get('password')

    user = User.query.filter_by(name=name).first()
    if user and check_password_hash(user.password, password):
        access_token = create_access_token(
            identity=user.user_id,
            expires_delta=timedelta(days=1)
        )
        return jsonify({
            'message': 'Login successful',
            'access_token': access_token,
            'user_id': user.user_id,
            'name': user.name,
            'photo_url': user.photo_url
        })
    return jsonify({'error': 'Invalid credentials'}), 401


@bp.route('/user/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get(user_id)
    if user:
        return jsonify({
            'user_id': user.user_id,
            'name': user.name,
            'photo_url': user.photo_url
        })
    return jsonify({'error': 'User not found'}), 404
