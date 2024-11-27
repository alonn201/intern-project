from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from auth.user import User

auth_blueprint = Blueprint('auth', __name__)

@auth_blueprint.route('/register', methods=['POST'])
def register():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
        
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
        
    valid, msg = User.validate(username)
    if not valid:
        return jsonify({"error": msg}), 400
        
    user = User(username=username, password=password)
    user.hash_password()
    
    user_id = user.save()
    if user_id:
        return jsonify({"message": "User registered successfully"}), 201
    return jsonify({"error": "Username may already be taken"}), 400

@auth_blueprint.route('/login', methods=['POST'])
def login():
    
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400
    
    user_id = User.authenticate(username, password)
    if user_id:
        # Generate JWT for the authenticated user
        access_token = create_access_token(identity=user_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"error": "Invalid credentials"}), 401