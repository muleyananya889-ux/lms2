from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
import bcrypt
import re

# Blueprints
auth_bp = Blueprint('auth', __name__)
courses_bp = Blueprint('courses', __name__)
lessons_bp = Blueprint('lessons', __name__)
enrollment_bp = Blueprint('enrollment', __name__)
progress_bp = Blueprint('progress', __name__)

# Helper functions
def validate_email(email):
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None

def validate_password(password):
    return len(password) >= 6

def get_db_connection():
    from flask import current_app
    return current_app.get_db_connection()

# Auth routes
@auth_bp.route('/signup', methods=['POST'])
def signup():
    try:
        data = request.get_json()
        
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
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            if cursor.fetchone():
                return jsonify({'error': 'User with this email already exists'}), 400
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute(
                "INSERT INTO users (name, email, password, role) VALUES (?, ?, ?, ?)",
                (name, email, hashed_password, role)
            )
            conn.commit()
            
            cursor.execute("SELECT user_id, name, email, role FROM users WHERE email = ?", (email,))
            new_user = dict(cursor.fetchone())
            
            access_token = create_access_token(identity=new_user['user_id'])
            
            return jsonify({
                'message': 'User created successfully',
                'user': new_user,
                'access_token': access_token
            }), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        
        if not data or not all(k in data for k in ('email', 'password')):
            return jsonify({'error': 'Email and password are required'}), 400
        
        email = data['email'].strip().lower()
        password = data['password']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE email = ?", (email,))
            user = dict(cursor.fetchone())
            
            if not user or not bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
                return jsonify({'error': 'Invalid email or password'}), 401
            
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
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@auth_bp.route('/me', methods=['GET'])
@jwt_required()
def get_current_user():
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute(
                "SELECT user_id, name, email, role, created_at FROM users WHERE user_id = ?",
                (user_id,)
            )
            user = dict(cursor.fetchone())
            
            if not user:
                return jsonify({'error': 'User not found'}), 404
            
            return jsonify({'user': user}), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Courses routes
@courses_bp.route('/', methods=['GET', 'OPTIONS'])
@courses_bp.route('', methods=['GET', 'OPTIONS'])
def get_all_courses():
    # Handle OPTIONS request for CORS
    if request.method == 'OPTIONS':
        return '', 200
        
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, u.name as instructor_name,
                       (SELECT COUNT(*) FROM enrollments WHERE course_id = c.course_id) as enrollment_count
                FROM courses c
                LEFT JOIN users u ON c.instructor_id = u.user_id
                ORDER BY c.created_at DESC
            ''')
            courses = [dict(row) for row in cursor.fetchall()]
            
            formatted_courses = []
            for course in courses:
                formatted_course = {
                    'id': course['course_id'],
                    'title': course['title'],
                    'description': course['description'],
                    'thumbnail': course['thumbnail'],
                    'category': course['category'],
                    'instructor_name': course['instructor_name'] or 'Unknown',
                    'total_lessons': course['total_lessons'],
                    'total_duration': course['total_duration'],
                    'enrollment_count': course['enrollment_count'],
                    'created_at': course['created_at']
                }
                formatted_courses.append(formatted_course)
            
            return jsonify({'courses': formatted_courses}), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT c.*, u.name as instructor_name
                FROM courses c
                LEFT JOIN users u ON c.instructor_id = u.user_id
                WHERE c.course_id = ?
            ''', (course_id,))
            course = dict(cursor.fetchone())
            
            if not course:
                return jsonify({'error': 'Course not found'}), 404
            
            cursor.execute('''
                SELECT s.section_id, s.title as section_title, s.order_number as section_order,
                       l.lesson_id, l.title as lesson_title, l.order_number as lesson_order,
                       l.youtube_url, l.duration
                FROM sections s
                LEFT JOIN lessons l ON s.section_id = l.section_id
                WHERE s.course_id = ?
                ORDER BY s.order_number, l.order_number
            ''', (course_id,))
            sections_lessons = [dict(row) for row in cursor.fetchall()]
            
            sections = {}
            for item in sections_lessons:
                section_id = item['section_id']
                if section_id not in sections:
                    sections[section_id] = {
                        'id': section_id,
                        'title': item['section_title'],
                        'order': item['section_order'],
                        'lessons': []
                    }
                
                if item['lesson_id']:
                    sections[section_id]['lessons'].append({
                        'id': item['lesson_id'],
                        'title': item['lesson_title'],
                        'order': item['lesson_order'],
                        'youtube_url': item['youtube_url'],
                        'duration': item['duration']
                    })
            
            course_details = {
                'id': course['course_id'],
                'title': course['title'],
                'description': course['description'],
                'thumbnail': course['thumbnail'],
                'category': course['category'],
                'instructor_name': course['instructor_name'] or 'Unknown',
                'total_lessons': course['total_lessons'],
                'total_duration': course['total_duration'],
                'sections': list(sections.values()),
                'created_at': course['created_at']
            }
            
            return jsonify({'course': course_details}), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Enrollment routes
@enrollment_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_course():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or 'course_id' not in data:
            return jsonify({'error': 'Course ID is required'}), 400
        
        course_id = data['course_id']
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM courses WHERE course_id = ?", (course_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Course not found'}), 404
            
            cursor.execute("SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?", (user_id, course_id))
            if cursor.fetchone():
                return jsonify({'error': 'Already enrolled in this course'}), 400
            
            cursor.execute("INSERT INTO enrollments (user_id, course_id) VALUES (?, ?)", (user_id, course_id))
            conn.commit()
            
            return jsonify({'message': 'Enrolled successfully'}), 201
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@enrollment_bp.route('/check/<int:course_id>', methods=['GET'])
@jwt_required()
def check_enrollment(course_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?", (user_id, course_id))
            enrollment = cursor.fetchone()
            
            if enrollment:
                return jsonify({'enrolled': True}), 200
            else:
                return jsonify({'enrolled': False}), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Progress routes
@progress_bp.route('/update', methods=['POST'])
@jwt_required()
def update_progress():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        if not data or not all(k in data for k in ('course_id', 'lesson_id', 'status')):
            return jsonify({'error': 'Course ID, lesson ID, and status are required'}), 400
        
        course_id = data['course_id']
        lesson_id = data['lesson_id']
        status = data['status']
        
        if status not in ['completed', 'in_progress']:
            return jsonify({'error': 'Status must be either completed or in_progress'}), 400
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?", (user_id, course_id))
            if not cursor.fetchone():
                return jsonify({'error': 'Not enrolled in this course'}), 403
            
            cursor.execute('''
                SELECT l.lesson_id 
                FROM lessons l
                JOIN sections s ON l.section_id = s.section_id
                WHERE l.lesson_id = ? AND s.course_id = ?
            ''', (lesson_id, course_id))
            if not cursor.fetchone():
                return jsonify({'error': 'Lesson not found in this course'}), 404
            
            cursor.execute("SELECT * FROM progress WHERE user_id = ? AND lesson_id = ?", (user_id, lesson_id))
            if cursor.fetchone():
                cursor.execute('''
                    UPDATE progress 
                    SET status = ?, last_watched = CURRENT_TIMESTAMP 
                    WHERE user_id = ? AND lesson_id = ?
                ''', (status, user_id, lesson_id))
            else:
                cursor.execute('''
                    INSERT INTO progress (user_id, course_id, lesson_id, status)
                    VALUES (?, ?, ?, ?)
                ''', (user_id, course_id, lesson_id, status))
            
            conn.commit()
            
            return jsonify({'message': 'Progress updated successfully'}), 200
            
        except Exception as e:
            conn.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@progress_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_progress(course_id):
    try:
        user_id = get_jwt_identity()
        
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM enrollments WHERE user_id = ? AND course_id = ?", (user_id, course_id))
            if not cursor.fetchone():
                return jsonify({'error': 'Not enrolled in this course'}), 403
            
            cursor.execute('''
                SELECT 
                    COUNT(*) as total_lessons,
                    SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_lessons,
                    MAX(last_watched) as last_watched
                FROM progress
                WHERE user_id = ? AND course_id = ?
            ''', (user_id, course_id))
            overall_progress = dict(cursor.fetchone())
            
            cursor.execute("SELECT total_lessons FROM courses WHERE course_id = ?", (course_id,))
            course_info = dict(cursor.fetchone())
            
            total_lessons = course_info['total_lessons'] if course_info else 0
            completed_lessons = overall_progress['completed_lessons'] or 0
            progress_percentage = 0
            if total_lessons > 0:
                progress_percentage = round((completed_lessons / total_lessons) * 100)
            
            return jsonify({
                'progress': {
                    'total_lessons': total_lessons,
                    'completed_lessons': completed_lessons,
                    'percentage': progress_percentage,
                    'last_watched': overall_progress['last_watched']
                }
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

# Lessons routes
@lessons_bp.route('/courses/<int:course_id>/lessons', methods=['GET'])
def get_course_lessons(course_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT course_id FROM courses WHERE course_id = ?", (course_id,))
            if not cursor.fetchone():
                return jsonify({'error': 'Course not found'}), 404
            
            cursor.execute('''
                SELECT s.section_id, s.title as section_title, s.order_number as section_order,
                       l.lesson_id, l.title as lesson_title, l.order_number as lesson_order,
                       l.youtube_url, l.duration
                FROM sections s
                LEFT JOIN lessons l ON s.section_id = l.section_id
                WHERE s.course_id = ?
                ORDER BY s.order_number, l.order_number
            ''', (course_id,))
            results = [dict(row) for row in cursor.fetchall()]
            
            sections = {}
            for item in results:
                section_id = item['section_id']
                if section_id not in sections:
                    sections[section_id] = {
                        'id': section_id,
                        'title': item['section_title'],
                        'order': item['section_order'],
                        'lessons': []
                    }
                
                if item['lesson_id']:
                    sections[section_id]['lessons'].append({
                        'id': item['lesson_id'],
                        'title': item['lesson_title'],
                        'order': item['lesson_order'],
                        'youtube_url': item['youtube_url'],
                        'duration': item['duration']
                    })
            
            return jsonify({
                'course_id': course_id,
                'sections': list(sections.values())
            }), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@lessons_bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson_details(lesson_id):
    try:
        conn = get_db_connection()
        if not conn:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT l.*, s.title as section_title, s.course_id,
                       c.title as course_title, c.instructor_id
                FROM lessons l
                JOIN sections s ON l.section_id = s.section_id
                JOIN courses c ON s.course_id = c.course_id
                WHERE l.lesson_id = ?
            ''', (lesson_id,))
            lesson = dict(cursor.fetchone())
            
            if not lesson:
                return jsonify({'error': 'Lesson not found'}), 404
            
            cursor.execute('''
                SELECT lesson_id, title, order_number
                FROM lessons
                WHERE section_id = ? AND order_number < ?
                ORDER BY order_number DESC
                LIMIT 1
            ''', (lesson['section_id'], lesson['order_number']))
            previous_lesson = dict(cursor.fetchone()) if cursor.fetchone() else None
            
            cursor.execute('''
                SELECT lesson_id, title, order_number
                FROM lessons
                WHERE section_id = ? AND order_number > ?
                ORDER BY order_number ASC
                LIMIT 1
            ''', (lesson['section_id'], lesson['order_number']))
            next_lesson = dict(cursor.fetchone()) if cursor.fetchone() else None
            
            youtube_url = lesson['youtube_url']
            video_id = None
            if 'youtube.com/watch?v=' in youtube_url:
                video_id = youtube_url.split('v=')[1].split('&')[0]
            elif 'youtu.be/' in youtube_url:
                video_id = youtube_url.split('youtu.be/')[1].split('?')[0]
            
            lesson_details = {
                'id': lesson['lesson_id'],
                'title': lesson['title'],
                'youtube_url': lesson['youtube_url'],
                'video_id': video_id,
                'duration': lesson['duration'],
                'section': {
                    'id': lesson['section_id'],
                    'title': lesson['section_title']
                },
                'course': {
                    'id': lesson['course_id'],
                    'title': lesson['course_title'],
                    'instructor_id': lesson['instructor_id']
                },
                'navigation': {
                    'previous': previous_lesson,
                    'next': next_lesson
                }
            }
            
            return jsonify({'lesson': lesson_details}), 200
            
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            conn.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
