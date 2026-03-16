from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

courses_bp = Blueprint('courses', __name__)

@courses_bp.route('/', methods=['GET'])
def get_all_courses():
    try:
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Get all courses with instructor information
                cursor.execute("""
                    SELECT c.*, u.name as instructor_name,
                           (SELECT COUNT(*) FROM enrollments WHERE course_id = c.course_id) as enrollment_count
                    FROM courses c
                    LEFT JOIN users u ON c.instructor_id = u.user_id
                    ORDER BY c.created_at DESC
                """)
                courses = cursor.fetchall()
                
                # Format the response
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
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@courses_bp.route('/<int:course_id>', methods=['GET'])
def get_course_details(course_id):
    try:
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Get course details with instructor information
                cursor.execute("""
                    SELECT c.*, u.name as instructor_name, u.email as instructor_email
                    FROM courses c
                    LEFT JOIN users u ON c.instructor_id = u.user_id
                    WHERE c.course_id = %s
                """, (course_id,))
                course = cursor.fetchone()
                
                if not course:
                    return jsonify({'error': 'Course not found'}), 404
                
                # Get course sections and lessons
                cursor.execute("""
                    SELECT s.section_id, s.title as section_title, s.order_number as section_order,
                           l.lesson_id, l.title as lesson_title, l.order_number as lesson_order,
                           l.youtube_url, l.duration
                    FROM sections s
                    LEFT JOIN lessons l ON s.section_id = l.section_id
                    WHERE s.course_id = %s
                    ORDER BY s.order_number, l.order_number
                """, (course_id,))
                sections_lessons = cursor.fetchall()
                
                # Organize sections and lessons
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
                
                # Format the response
                course_details = {
                    'id': course['course_id'],
                    'title': course['title'],
                    'description': course['description'],
                    'thumbnail': course['thumbnail'],
                    'category': course['category'],
                    'instructor_name': course['instructor_name'] or 'Unknown',
                    'instructor_email': course['instructor_email'],
                    'total_lessons': course['total_lessons'],
                    'total_duration': course['total_duration'],
                    'sections': list(sections.values()),
                    'created_at': course['created_at']
                }
                
                return jsonify({'course': course_details}), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@courses_bp.route('/', methods=['POST'])
@jwt_required()
def create_course():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('title', 'description', 'category')):
            return jsonify({'error': 'Title, description, and category are required'}), 400
        
        title = data['title'].strip()
        description = data['description'].strip()
        category = data['category'].strip()
        thumbnail = data.get('thumbnail', '').strip()
        
        if not title or not description or not category:
            return jsonify({'error': 'Title, description, and category are required'}), 400
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user is instructor or admin
                cursor.execute("SELECT role FROM users WHERE user_id = %s", (user_id,))
                user = cursor.fetchone()
                
                if not user or user['role'] not in ['instructor', 'admin']:
                    return jsonify({'error': 'Only instructors and admins can create courses'}), 403
                
                # Insert new course
                cursor.execute(
                    """INSERT INTO courses (title, description, thumbnail, category, instructor_id) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (title, description, thumbnail, category, user_id)
                )
                
                connection.commit()
                
                # Get the newly created course
                cursor.execute("SELECT * FROM courses WHERE course_id = LAST_INSERT_ID()")
                new_course = cursor.fetchone()
                
                return jsonify({
                    'message': 'Course created successfully',
                    'course': {
                        'id': new_course['course_id'],
                        'title': new_course['title'],
                        'description': new_course['description'],
                        'thumbnail': new_course['thumbnail'],
                        'category': new_course['category'],
                        'instructor_id': new_course['instructor_id'],
                        'total_lessons': new_course['total_lessons'],
                        'total_duration': new_course['total_duration'],
                        'created_at': new_course['created_at']
                    }
                }), 201
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@courses_bp.route('/<int:course_id>', methods=['PUT'])
@jwt_required()
def update_course(course_id):
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user is the instructor or admin
                cursor.execute("""
                    SELECT c.*, u.role 
                    FROM courses c
                    JOIN users u ON c.instructor_id = u.user_id
                    WHERE c.course_id = %s
                """, (course_id,))
                course = cursor.fetchone()
                
                if not course:
                    return jsonify({'error': 'Course not found'}), 404
                
                if course['instructor_id'] != user_id and course['role'] != 'admin':
                    return jsonify({'error': 'Only course instructor or admin can update this course'}), 403
                
                # Update course
                update_fields = []
                update_values = []
                
                if 'title' in data and data['title'].strip():
                    update_fields.append("title = %s")
                    update_values.append(data['title'].strip())
                
                if 'description' in data and data['description'].strip():
                    update_fields.append("description = %s")
                    update_values.append(data['description'].strip())
                
                if 'category' in data and data['category'].strip():
                    update_fields.append("category = %s")
                    update_values.append(data['category'].strip())
                
                if 'thumbnail' in data:
                    update_fields.append("thumbnail = %s")
                    update_values.append(data['thumbnail'].strip())
                
                if not update_fields:
                    return jsonify({'error': 'No valid fields to update'}), 400
                
                update_values.append(course_id)
                
                cursor.execute(f"UPDATE courses SET {', '.join(update_fields)} WHERE course_id = %s", update_values)
                connection.commit()
                
                # Get updated course
                cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
                updated_course = cursor.fetchone()
                
                return jsonify({
                    'message': 'Course updated successfully',
                    'course': {
                        'id': updated_course['course_id'],
                        'title': updated_course['title'],
                        'description': updated_course['description'],
                        'thumbnail': updated_course['thumbnail'],
                        'category': updated_course['category'],
                        'instructor_id': updated_course['instructor_id'],
                        'total_lessons': updated_course['total_lessons'],
                        'total_duration': updated_course['total_duration'],
                        'updated_at': updated_course['updated_at']
                    }
                }), 200
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
