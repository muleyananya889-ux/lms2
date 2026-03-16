from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import re

auth_bp = Blueprint('auth', __name__)

def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('name', 'email', 'password', 'role')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        name = data['name'].strip()
        email = data['email'].strip().lower()
        password = data['password']
        role = data['role']
        
        if not name or not email or not password:
            return jsonify({'error': 'All fields are required'}), 400
        
        if not validate_email(email):
            return jsonify({'error': 'Invalid email format'}), 400
        
        if not validate_password(password):
            return jsonify({'error': 'Password must be at least 6 characters long'}), 400
        
        if role not in ['student', 'instructor', 'admin']:
            return jsonify({'error': 'Invalid role'}), 400
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user already exists
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                existing_user = cursor.fetchone()
                
                if existing_user:
                    return jsonify({'error': 'User with this email already exists'}), 400
                
                # Hash password
                hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (name, email, password, role) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_password, role)
                )
                
                connection.commit()
                
                # Get the newly created user
                cursor.execute("SELECT user_id, name, email, role FROM users WHERE email = %s", (email,))
                new_user = cursor.fetchone()
                
                # Create access token
                access_token = create_access_token(identity=new_user['user_id'])
                
                return jsonify({
                    'message': 'User created successfully',
                    'user': {
                        'id': new_user['user_id'],
                        'name': new_user['name'],
                        'email': new_user['email'],
                        'role': new_user['role']
                    },
                    'access_token': access_token
                }), 201
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        if not email or not password:
            return jsonify({'error': 'Email and password are required'}), 400
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Find user by email
                cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
                user = cursor.fetchone()
                
                if not user:
                    return jsonify({'error': 'Invalid email or password'}), 401
                
                # Verify password
                if not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                    return jsonify({'error': 'Invalid email or password'}), 401
                
                # Create access token
                access_token = create_access_token(identity=user['user_id'])
                
                return jsonify({
                    'message': 'Login successful',
                    'user': {
                        'id': user['user_id'],
                        'name': user['name'],
                        'email': user['email'],
                        'role': user['role']
                    },
                    'access_token': access_token
                }), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                cursor.execute(
                    "SELECT user_id, name, email, role, created_at FROM users WHERE user_id = %s",
                    (user_id,)
                )
                user = cursor.fetchone()
                
                if not user:
                    return jsonify({'error': 'User not found'}), 404
                
                return jsonify({
                    'user': {
                        'id': user['user_id'],
                        'name': user['name'],
                        'email': user['email'],
                        'role': user['role'],
                        'created_at': user['created_at']
                    }
                }), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
