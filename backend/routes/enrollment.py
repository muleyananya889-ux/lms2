from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

enrollment_bp = Blueprint('enrollment', __name__)

@enrollment_bp.route('/enroll', methods=['POST'])
@jwt_required()
def enroll_course():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or 'course_id' not in data:
            return jsonify({'error': 'Course ID is required'}), 400
        
        course_id = data['course_id']
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if course exists
                cursor.execute("SELECT * FROM courses WHERE course_id = %s", (course_id,))
                course = cursor.fetchone()
                
                if not course:
                    return jsonify({'error': 'Course not found'}), 404
                
                # Check if user is already enrolled
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                existing_enrollment = cursor.fetchone()
                
                if existing_enrollment:
                    return jsonify({'error': 'Already enrolled in this course'}), 400
                
                # Check if user is the instructor
                if course['instructor_id'] == user_id:
                    return jsonify({'error': 'Instructor cannot enroll in their own course'}), 400
                
                # Create enrollment
                cursor.execute("INSERT INTO enrollments (user_id, course_id) VALUES (%s, %s)", (user_id, course_id))
                connection.commit()
                
                # Get enrollment details
                cursor.execute("""
                    SELECT e.*, c.title, c.description, c.thumbnail, u.name as instructor_name
                    FROM enrollments e
                    JOIN courses c ON e.course_id = c.course_id
                    JOIN users u ON c.instructor_id = u.user_id
                    WHERE e.user_id = %s AND e.course_id = %s
                """, (user_id, course_id))
                enrollment = cursor.fetchone()
                
                return jsonify({
                    'message': 'Enrolled successfully',
                    'enrollment': {
                        'id': enrollment['enrollment_id'],
                        'course_id': enrollment['course_id'],
                        'course_title': enrollment['title'],
                        'course_description': enrollment['description'],
                        'course_thumbnail': enrollment['thumbnail'],
                        'instructor_name': enrollment['instructor_name'],
                        'enrollment_date': enrollment['enrollment_date']
                    }
                }), 201
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@enrollment_bp.route('/user/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_enrollments(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only see their own enrollments (except admins)
        if current_user_id != user_id:
            # Check if current user is admin
            from flask import current_app
            connection = current_app.get_db_connection()
            if not connection:
                return jsonify({'error': 'Database connection failed'}), 500
            
            try:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT role FROM users WHERE user_id = %s", (current_user_id,))
                    user = cursor.fetchone()
                    
                    if not user or user['role'] != 'admin':
                        return jsonify({'error': 'Access denied'}), 403
            finally:
                connection.close()
        
        # Get database connection
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Get user enrollments with course details and progress
                cursor.execute("""
                    SELECT e.*, c.title, c.description, c.thumbnail, c.category,
                           c.total_lessons, c.total_duration, u.name as instructor_name,
                           (SELECT COUNT(*) FROM progress p WHERE p.user_id = e.user_id AND p.course_id = e.course_id AND p.status = 'completed') as completed_lessons
                    FROM enrollments e
                    JOIN courses c ON e.course_id = c.course_id
                    JOIN users u ON c.instructor_id = u.user_id
                    WHERE e.user_id = %s
                    ORDER BY e.enrollment_date DESC
                """, (user_id,))
                enrollments = cursor.fetchall()
                
                # Format enrollments with progress
                formatted_enrollments = []
                for enrollment in enrollments:
                    progress_percentage = 0
                    if enrollment['total_lessons'] > 0:
                        progress_percentage = round((enrollment['completed_lessons'] / enrollment['total_lessons']) * 100)
                    
                    formatted_enrollment = {
                        'id': enrollment['enrollment_id'],
                        'course': {
                            'id': enrollment['course_id'],
                            'title': enrollment['title'],
                            'description': enrollment['description'],
                            'thumbnail': enrollment['thumbnail'],
                            'category': enrollment['category'],
                            'instructor_name': enrollment['instructor_name'],
                            'total_lessons': enrollment['total_lessons'],
                            'total_duration': enrollment['total_duration']
                        },
                        'progress': {
                            'completed_lessons': enrollment['completed_lessons'],
                            'total_lessons': enrollment['total_lessons'],
                            'percentage': progress_percentage
                        },
                        'enrollment_date': enrollment['enrollment_date']
                    }
                    formatted_enrollments.append(formatted_enrollment)
                
                return jsonify({'enrollments': formatted_enrollments}), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@enrollment_bp.route('/course/<int:course_id>/students', methods=['GET'])
@jwt_required()
def get_course_students(course_id):
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user is the instructor or admin
                cursor.execute("""
                    SELECT c.instructor_id, u.role
                    FROM courses c
                    JOIN users u ON u.user_id = %s
                    WHERE c.course_id = %s
                """, (user_id, course_id))
                result = cursor.fetchone()
                
                if not result:
                    return jsonify({'error': 'Course not found'}), 404
                
                if result['instructor_id'] != user_id and result['role'] != 'admin':
                    return jsonify({'error': 'Access denied'}), 403
                
                # Get enrolled students with progress
                cursor.execute("""
                    SELECT u.user_id, u.name, u.email, e.enrollment_date,
                           (SELECT COUNT(*) FROM progress p WHERE p.user_id = u.user_id AND p.course_id = %s AND p.status = 'completed') as completed_lessons
                    FROM enrollments e
                    JOIN users u ON e.user_id = u.user_id
                    WHERE e.course_id = %s
                    ORDER BY e.enrollment_date DESC
                """, (course_id, course_id))
                students = cursor.fetchone()
                
                # Get course total lessons for progress calculation
                cursor.execute("SELECT total_lessons FROM courses WHERE course_id = %s", (course_id,))
                course = cursor.fetchone()
                total_lessons = course['total_lessons'] if course else 0
                
                # Format students with progress
                formatted_students = []
                for student in students:
                    progress_percentage = 0
                    if total_lessons > 0:
                        progress_percentage = round((student['completed_lessons'] / total_lessons) * 100)
                    
                    formatted_student = {
                        'id': student['user_id'],
                        'name': student['name'],
                        'email': student['email'],
                        'progress': {
                            'completed_lessons': student['completed_lessons'],
                            'total_lessons': total_lessons,
                            'percentage': progress_percentage
                        },
                        'enrollment_date': student['enrollment_date']
                    }
                    formatted_students.append(formatted_student)
                
                return jsonify({'students': formatted_students}), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@enrollment_bp.route('/unenroll', methods=['DELETE'])
@jwt_required()
def unenroll_course():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or 'course_id' not in data:
            return jsonify({'error': 'Course ID is required'}), 400
        
        course_id = data['course_id']
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if enrollment exists
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                enrollment = cursor.fetchone()
                
                if not enrollment:
                    return jsonify({'error': 'Not enrolled in this course'}), 404
                
                # Delete enrollment
                cursor.execute("DELETE FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                
                # Delete related progress records
                cursor.execute("DELETE FROM progress WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                
                connection.commit()
                
                return jsonify({'message': 'Unenrolled successfully'}), 200
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@enrollment_bp.route('/check/<int:course_id>', methods=['GET'])
@jwt_required()
def check_enrollment(course_id):
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user is enrolled
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                enrollment = cursor.fetchone()
                
                if enrollment:
                    return jsonify({'enrolled': True, 'enrollment_date': enrollment['enrollment_date']}), 200
                else:
                    return jsonify({'enrolled': False}), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
