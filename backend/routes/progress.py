from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime

progress_bp = Blueprint('progress', __name__)

@progress_bp.route('/update', methods=['POST'])
@jwt_required()
def update_progress():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('course_id', 'lesson_id', 'status')):
            return jsonify({'error': 'Course ID, lesson ID, and status are required'}), 400
        
        course_id = data['course_id']
        lesson_id = data['lesson_id']
        status = data['status']
        
        if status not in ['completed', 'in_progress']:
            return jsonify({'error': 'Status must be either completed or in_progress'}), 400
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Verify user is enrolled in the course
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                if not cursor.fetchone():
                    return jsonify({'error': 'Not enrolled in this course'}), 403
                
                # Verify lesson belongs to the course
                cursor.execute("""
                    SELECT l.lesson_id 
                    FROM lessons l
                    JOIN sections s ON l.section_id = s.section_id
                    WHERE l.lesson_id = %s AND s.course_id = %s
                """, (lesson_id, course_id))
                if not cursor.fetchone():
                    return jsonify({'error': 'Lesson not found in this course'}), 404
                
                # Check if progress record exists
                cursor.execute("SELECT * FROM progress WHERE user_id = %s AND lesson_id = %s", (user_id, lesson_id))
                existing_progress = cursor.fetchone()
                
                if existing_progress:
                    # Update existing progress
                    cursor.execute("""
                        UPDATE progress 
                        SET status = %s, last_watched = CURRENT_TIMESTAMP 
                        WHERE user_id = %s AND lesson_id = %s
                    """, (status, user_id, lesson_id))
                else:
                    # Create new progress record
                    cursor.execute("""
                        INSERT INTO progress (user_id, course_id, lesson_id, status)
                        VALUES (%s, %s, %s, %s)
                    """, (user_id, course_id, lesson_id, status))
                
                connection.commit()
                
                # Get updated progress statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_lessons,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_lessons
                    FROM progress
                    WHERE user_id = %s AND course_id = %s
                """, (user_id, course_id))
                progress_stats = cursor.fetchone()
                
                # Calculate progress percentage
                progress_percentage = 0
                if progress_stats['total_lessons'] > 0:
                    progress_percentage = round((progress_stats['completed_lessons'] / progress_stats['total_lessons']) * 100)
                
                return jsonify({
                    'message': 'Progress updated successfully',
                    'progress': {
                        'total_lessons': progress_stats['total_lessons'],
                        'completed_lessons': progress_stats['completed_lessons'],
                        'percentage': progress_percentage
                    }
                }), 200
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@progress_bp.route('/<int:course_id>', methods=['GET'])
@jwt_required()
def get_course_progress(course_id):
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Verify user is enrolled in the course
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                if not cursor.fetchone():
                    return jsonify({'error': 'Not enrolled in this course'}), 403
                
                # Get overall progress statistics
                cursor.execute("""
                    SELECT 
                        COUNT(*) as total_lessons,
                        SUM(CASE WHEN status = 'completed' THEN 1 ELSE 0 END) as completed_lessons,
                        MAX(last_watched) as last_watched
                    FROM progress
                    WHERE user_id = %s AND course_id = %s
                """, (user_id, course_id))
                overall_progress = cursor.fetchone()
                
                # Get course total lessons from courses table
                cursor.execute("SELECT total_lessons FROM courses WHERE course_id = %s", (course_id,))
                course_info = cursor.fetchone()
                
                # Calculate progress percentage
                total_lessons = course_info['total_lessons'] if course_info else 0
                completed_lessons = overall_progress['completed_lessons'] or 0
                progress_percentage = 0
                if total_lessons > 0:
                    progress_percentage = round((completed_lessons / total_lessons) * 100)
                
                # Get detailed progress for all lessons
                cursor.execute("""
                    SELECT l.lesson_id, l.title, l.section_id, s.title as section_title,
                           l.order_number, s.order_number as section_order,
                           COALESCE(p.status, 'not_started') as status,
                           p.last_watched
                    FROM lessons l
                    JOIN sections s ON l.section_id = s.section_id
                    LEFT JOIN progress p ON l.lesson_id = p.lesson_id AND p.user_id = %s
                    WHERE s.course_id = %s
                    ORDER BY s.order_number, l.order_number
                """, (user_id, course_id))
                lesson_progress = cursor.fetchall()
                
                # Find last watched lesson
                last_watched_lesson = None
                if overall_progress['last_watched']:
                    cursor.execute("""
                        SELECT l.lesson_id, l.title, l.section_id, s.title as section_title
                        FROM progress p
                        JOIN lessons l ON p.lesson_id = l.lesson_id
                        JOIN sections s ON l.section_id = s.section_id
                        WHERE p.user_id = %s AND p.course_id = %s AND p.last_watched = %s
                    """, (user_id, course_id, overall_progress['last_watched']))
                    last_watched_lesson = cursor.fetchone()
                
                return jsonify({
                    'progress': {
                        'total_lessons': total_lessons,
                        'completed_lessons': completed_lessons,
                        'percentage': progress_percentage,
                        'last_watched': overall_progress['last_watched'],
                        'last_watched_lesson': last_watched_lesson
                    },
                    'lessons': lesson_progress
                }), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@progress_bp.route('/lesson/<int:lesson_id>', methods=['GET'])
@jwt_required()
def get_lesson_progress(lesson_id):
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Get lesson progress
                cursor.execute("SELECT * FROM progress WHERE user_id = %s AND lesson_id = %s", (user_id, lesson_id))
                progress = cursor.fetchone()
                
                if progress:
                    return jsonify({
                        'progress': {
                            'lesson_id': progress['lesson_id'],
                            'course_id': progress['course_id'],
                            'status': progress['status'],
                            'last_watched': progress['last_watched']
                        }
                    }), 200
                else:
                    return jsonify({'progress': None, 'message': 'No progress found for this lesson'}), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@progress_bp.route('/dashboard/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user_dashboard_progress(user_id):
    try:
        current_user_id = get_jwt_identity()
        
        # Users can only see their own dashboard (except admins)
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
                # Get enrolled courses with progress
                cursor.execute("""
                    SELECT c.course_id, c.title, c.thumbnail, c.total_lessons,
                           COUNT(p.lesson_id) as completed_lessons,
                           MAX(p.last_watched) as last_activity
                    FROM enrollments e
                    JOIN courses c ON e.course_id = c.course_id
                    LEFT JOIN progress p ON e.course_id = p.course_id AND e.user_id = p.user_id AND p.status = 'completed'
                    WHERE e.user_id = %s
                    GROUP BY c.course_id, c.title, c.thumbnail, c.total_lessons
                    ORDER BY last_activity DESC, e.enrollment_date DESC
                """, (user_id,))
                courses_progress = cursor.fetchall()
                
                # Calculate statistics
                total_enrolled = len(courses_progress)
                total_completed = 0
                total_lessons_completed = 0
                total_lessons_all = 0
                
                formatted_courses = []
                for course in courses_progress:
                    completed_lessons = course['completed_lessons'] or 0
                    total_lessons = course['total_lessons'] or 0
                    progress_percentage = 0
                    
                    if total_lessons > 0:
                        progress_percentage = round((completed_lessons / total_lessons) * 100)
                        if progress_percentage == 100:
                            total_completed += 1
                    
                    total_lessons_completed += completed_lessons
                    total_lessons_all += total_lessons
                    
                    formatted_course = {
                        'id': course['course_id'],
                        'title': course['title'],
                        'thumbnail': course['thumbnail'],
                        'progress': {
                            'completed_lessons': completed_lessons,
                            'total_lessons': total_lessons,
                            'percentage': progress_percentage
                        },
                        'last_activity': course['last_activity']
                    }
                    formatted_courses.append(formatted_course)
                
                # Overall statistics
                overall_progress = 0
                if total_lessons_all > 0:
                    overall_progress = round((total_lessons_completed / total_lessons_all) * 100)
                
                return jsonify({
                    'statistics': {
                        'total_enrolled': total_enrolled,
                        'total_completed': total_completed,
                        'total_lessons_completed': total_lessons_completed,
                        'total_lessons_all': total_lessons_all,
                        'overall_progress': overall_progress
                    },
                    'courses': formatted_courses
                }), 200
                
        except Exception as e:
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@progress_bp.route('/reset/<int:course_id>', methods=['DELETE'])
@jwt_required()
def reset_course_progress(course_id):
    try:
        user_id = get_jwt_identity()
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Verify user is enrolled in the course
                cursor.execute("SELECT * FROM enrollments WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                if not cursor.fetchone():
                    return jsonify({'error': 'Not enrolled in this course'}), 403
                
                # Delete all progress for this course
                cursor.execute("DELETE FROM progress WHERE user_id = %s AND course_id = %s", (user_id, course_id))
                connection.commit()
                
                return jsonify({'message': 'Course progress reset successfully'}), 200
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
