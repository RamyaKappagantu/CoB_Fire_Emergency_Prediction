from flask import Flask, request, jsonify, Blueprint
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from database import db
from Models.user import User

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=['POST'])
@jwt_required()
def add_user():
    current_user = get_jwt_identity()
    if not current_user['is_admin']:
        return jsonify({"message": "Access denied"}), 403

    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required"}), 400

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"message": "Username already exists"}), 400

    hashed_password = generate_password_hash(data['password'], method='pbkdf2:sha256')
    is_admin = data.get('is_admin', False)
    if isinstance(is_admin, str):
        is_admin = is_admin.lower() in ['true', '1', 't', 'y', 'yes']

    new_user = User(username=data['username'], password=hashed_password, is_admin=is_admin)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully"}), 201

@bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return jsonify({"message": "Username and password are required"}), 400

    user = User.query.filter_by(username=data['username']).first()
    if not user or not check_password_hash(user.password, data['password']):
        return jsonify({"message": "Username and password does not exists"}), 401

    access_token = create_access_token(identity={"username": user.username, "is_admin": user.is_admin})
    return jsonify(access_token=access_token), 200
