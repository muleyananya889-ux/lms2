from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

lessons_bp = Blueprint('lessons', __name__)

@lessons_bp.route('/courses/<int:course_id>/lessons', methods=['GET'])
def get_course_lessons(course_id):
    try:
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Verify course exists
                cursor.execute("SELECT course_id FROM courses WHERE course_id = %s", (course_id,))
                if not cursor.fetchone():
                    return jsonify({'error': 'Course not found'}), 404
                
                # Get all lessons for the course with sections
                cursor.execute("""
                    SELECT s.section_id, s.title as section_title, s.order_number as section_order,
                           l.lesson_id, l.title as lesson_title, l.order_number as lesson_order,
                           l.youtube_url, l.duration
                    FROM sections s
                    LEFT JOIN lessons l ON s.section_id = l.section_id
                    WHERE s.course_id = %s
                    ORDER BY s.order_number, l.order_number
                """, (course_id,))
                results = cursor.fetchall()
                
                # Organize lessons by sections
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
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@lessons_bp.route('/<int:lesson_id>', methods=['GET'])
def get_lesson_details(lesson_id):
    try:
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Get lesson details with section and course info
                cursor.execute("""
                    SELECT l.*, s.title as section_title, s.course_id,
                           c.title as course_title, c.instructor_id
                    FROM lessons l
                    JOIN sections s ON l.section_id = s.section_id
                    JOIN courses c ON s.course_id = c.course_id
                    WHERE l.lesson_id = %s
                """, (lesson_id,))
                lesson = cursor.fetchone()
                
                if not lesson:
                    return jsonify({'error': 'Lesson not found'}), 404
                
                # Get previous and next lessons for navigation
                cursor.execute("""
                    SELECT lesson_id, title, order_number
                    FROM lessons
                    WHERE section_id = %s AND order_number < %s
                    ORDER BY order_number DESC
                    LIMIT 1
                """, (lesson['section_id'], lesson['order_number']))
                previous_lesson = cursor.fetchone()
                
                cursor.execute("""
                    SELECT lesson_id, title, order_number
                    FROM lessons
                    WHERE section_id = %s AND order_number > %s
                    ORDER BY order_number ASC
                    LIMIT 1
                """, (lesson['section_id'], lesson['order_number']))
                next_lesson = cursor.fetchone()
                
                # If no next lesson in current section, check first lesson of next section
                if not next_lesson:
                    cursor.execute("""
                        SELECT l.lesson_id, l.title, l.order_number
                        FROM lessons l
                        JOIN sections s ON l.section_id = s.section_id
                        WHERE s.course_id = %s AND s.order_number > %s
                        ORDER BY s.order_number ASC, l.order_number ASC
                        LIMIT 1
                    """, (lesson['course_id'], lesson['section_id']))
                    next_lesson = cursor.fetchone()
                
                # Extract YouTube video ID
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
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@lessons_bp.route('/', methods=['POST'])
@jwt_required()
def create_lesson():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        # Validate input
        if not data or not all(k in data for k in ('section_id', 'title', 'youtube_url')):
            return jsonify({'error': 'Section ID, title, and YouTube URL are required'}), 400
        
        section_id = data['section_id']
        title = data['title'].strip()
        youtube_url = data['youtube_url'].strip()
        duration = data.get('duration', 0)
        order_number = data.get('order_number')
        
        if not title or not youtube_url:
            return jsonify({'error': 'Title and YouTube URL are required'}), 400
        
        # Validate YouTube URL
        if not ('youtube.com/watch?v=' in youtube_url or 'youtu.be/' in youtube_url):
            return jsonify({'error': 'Invalid YouTube URL format'}), 400
        
        # Get database connection
        from flask import current_app
        connection = current_app.get_db_connection()
        if not connection:
            return jsonify({'error': 'Database connection failed'}), 500
        
        try:
            with connection.cursor() as cursor:
                # Check if user is instructor or admin and has permission for this course
                cursor.execute("""
                    SELECT c.instructor_id, u.role
                    FROM sections s
                    JOIN courses c ON s.course_id = c.course_id
                    JOIN users u ON u.user_id = %s
                    WHERE s.section_id = %s
                """, (user_id, section_id))
                result = cursor.fetchone()
                
                if not result:
                    return jsonify({'error': 'Section not found'}), 404
                
                if result['instructor_id'] != user_id and result['role'] != 'admin':
                    return jsonify({'error': 'Only course instructor or admin can add lessons'}), 403
                
                # If order_number not provided, get the next order number
                if order_number is None:
                    cursor.execute("SELECT MAX(order_number) as max_order FROM lessons WHERE section_id = %s", (section_id,))
                    max_order = cursor.fetchone()
                    order_number = (max_order['max_order'] or 0) + 1
                
                # Insert new lesson
                cursor.execute(
                    """INSERT INTO lessons (section_id, title, youtube_url, duration, order_number) 
                       VALUES (%s, %s, %s, %s, %s)""",
                    (section_id, title, youtube_url, duration, order_number)
                )
                
                connection.commit()
                
                # Update course total lessons and duration
                cursor.execute("""
                    UPDATE courses c SET 
                        total_lessons = (
                            SELECT COUNT(*) 
                            FROM lessons l 
                            JOIN sections s ON l.section_id = s.section_id 
                            WHERE s.course_id = c.course_id
                        ),
                        total_duration = (
                            SELECT COALESCE(SUM(duration), 0) 
                            FROM lessons l 
                            JOIN sections s ON l.section_id = s.section_id 
                            WHERE s.course_id = c.course_id
                        )
                    WHERE c.course_id = (SELECT course_id FROM sections WHERE section_id = %s)
                """, (section_id,))
                connection.commit()
                
                # Get the newly created lesson
                cursor.execute("SELECT * FROM lessons WHERE lesson_id = LAST_INSERT_ID()")
                new_lesson = cursor.fetchone()
                
                return jsonify({
                    'message': 'Lesson created successfully',
                    'lesson': {
                        'id': new_lesson['lesson_id'],
                        'section_id': new_lesson['section_id'],
                        'title': new_lesson['title'],
                        'youtube_url': new_lesson['youtube_url'],
                        'duration': new_lesson['duration'],
                        'order_number': new_lesson['order_number'],
                        'created_at': new_lesson['created_at']
                    }
                }), 201
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@lessons_bp.route('/<int:lesson_id>', methods=['PUT'])
@jwt_required()
def update_lesson(lesson_id):
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
                # Check if user has permission to update this lesson
                cursor.execute("""
                    SELECT l.*, c.instructor_id, u.role
                    FROM lessons l
                    JOIN sections s ON l.section_id = s.section_id
                    JOIN courses c ON s.course_id = c.course_id
                    JOIN users u ON u.user_id = %s
                    WHERE l.lesson_id = %s
                """, (user_id, lesson_id))
                lesson = cursor.fetchone()
                
                if not lesson:
                    return jsonify({'error': 'Lesson not found'}), 404
                
                if lesson['instructor_id'] != user_id and lesson['role'] != 'admin':
                    return jsonify({'error': 'Only course instructor or admin can update this lesson'}), 403
                
                # Update lesson
                update_fields = []
                update_values = []
                
                if 'title' in data and data['title'].strip():
                    update_fields.append("title = %s")
                    update_values.append(data['title'].strip())
                
                if 'youtube_url' in data and data['youtube_url'].strip():
                    youtube_url = data['youtube_url'].strip()
                    if not ('youtube.com/watch?v=' in youtube_url or 'youtu.be/' in youtube_url):
                        return jsonify({'error': 'Invalid YouTube URL format'}), 400
                    update_fields.append("youtube_url = %s")
                    update_values.append(youtube_url)
                
                if 'duration' in data and isinstance(data['duration'], int) and data['duration'] >= 0:
                    update_fields.append("duration = %s")
                    update_values.append(data['duration'])
                
                if 'order_number' in data and isinstance(data['order_number'], int) and data['order_number'] > 0:
                    update_fields.append("order_number = %s")
                    update_values.append(data['order_number'])
                
                if not update_fields:
                    return jsonify({'error': 'No valid fields to update'}), 400
                
                update_values.append(lesson_id)
                
                cursor.execute(f"UPDATE lessons SET {', '.join(update_fields)} WHERE lesson_id = %s", update_values)
                connection.commit()
                
                # Update course totals if duration changed
                if 'duration' in data:
                    cursor.execute("""
                        UPDATE courses c SET 
                            total_duration = (
                                SELECT COALESCE(SUM(duration), 0) 
                                FROM lessons l 
                                JOIN sections s ON l.section_id = s.section_id 
                                WHERE s.course_id = c.course_id
                            )
                        WHERE c.course_id = (SELECT course_id FROM sections WHERE section_id = %s)
                    """, (lesson['section_id']))
                    connection.commit()
                
                # Get updated lesson
                cursor.execute("SELECT * FROM lessons WHERE lesson_id = %s", (lesson_id,))
                updated_lesson = cursor.fetchone()
                
                return jsonify({
                    'message': 'Lesson updated successfully',
                    'lesson': {
                        'id': updated_lesson['lesson_id'],
                        'section_id': updated_lesson['section_id'],
                        'title': updated_lesson['title'],
                        'youtube_url': updated_lesson['youtube_url'],
                        'duration': updated_lesson['duration'],
                        'order_number': updated_lesson['order_number'],
                        'updated_at': updated_lesson['updated_at']
                    }
                }), 200
                
        except Exception as e:
            connection.rollback()
            return jsonify({'error': f'Database error: {str(e)}'}), 500
        finally:
            connection.close()
            
    except Exception as e:
        return jsonify({'error': f'Server error: {str(e)}'}), 500
