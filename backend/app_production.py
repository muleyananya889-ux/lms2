from flask import Flask, jsonify
from flask_cors import CORS
from flask_jwt_extended import JWTManager
import sqlite3
from datetime import datetime
from production_config import ProductionConfig

def create_app():
    app = Flask(__name__)
    app.config.from_object(ProductionConfig)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Enable CORS with production settings
    CORS(app, origins=app.config['CORS_ORIGINS'], supports_credentials=True)
    
    # Database connection helper
    def get_db_connection():
        try:
            conn = sqlite3.connect(app.config['SQLALCHEMY_DATABASE_URI'])
            conn.row_factory = sqlite3.Row
            return conn
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    app.get_db_connection = get_db_connection
    
    # Initialize database with sample data
    def init_db():
        conn = get_db_connection()
        if conn:
            cursor = conn.cursor()
            
            # Create tables
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    email TEXT UNIQUE NOT NULL,
                    password TEXT NOT NULL,
                    role TEXT DEFAULT 'student',
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS courses (
                    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT,
                    thumbnail TEXT,
                    category TEXT,
                    instructor_id INTEGER,
                    total_lessons INTEGER DEFAULT 0,
                    total_duration INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (instructor_id) REFERENCES users (user_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS sections (
                    section_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    course_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    order_number INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (course_id) REFERENCES courses (course_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS lessons (
                    lesson_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    section_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    order_number INTEGER NOT NULL,
                    youtube_url TEXT NOT NULL,
                    duration INTEGER DEFAULT 0,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (section_id) REFERENCES sections (section_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS enrollments (
                    enrollment_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (course_id) REFERENCES courses (course_id),
                    UNIQUE (user_id, course_id)
                )
            ''')
            
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS progress (
                    progress_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    course_id INTEGER NOT NULL,
                    lesson_id INTEGER NOT NULL,
                    status TEXT DEFAULT 'in_progress',
                    last_watched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (user_id),
                    FOREIGN KEY (course_id) REFERENCES courses (course_id),
                    FOREIGN KEY (lesson_id) REFERENCES lessons (lesson_id),
                    UNIQUE (user_id, lesson_id)
                )
            ''')
            
            # Check if data exists
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                # Insert sample data
                cursor.execute('''
                    INSERT INTO users (name, email, password, role) VALUES
                    ('John Doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'instructor'),
                    ('Jane Smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'student'),
                    ('Admin User', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'admin')
                ''')
                
                cursor.execute('''
                    INSERT INTO courses (title, description, thumbnail, category, instructor_id, total_lessons, total_duration) VALUES
                    ('Introduction to React', 'Learn the basics of React.js including components, props, state, and hooks.', 'https://picsum.photos/400/200?random=1', 'Programming', 1, 6, 150),
                    ('Python for Beginners', 'Start your programming journey with Python fundamentals and basic concepts.', 'https://picsum.photos/400/200?random=2', 'Programming', 1, 4, 110),
                    ('Web Development Fundamentals', 'Master HTML, CSS, and JavaScript to build modern websites.', 'https://picsum.photos/400/200?random=3', 'Web Development', 1, 4, 130)
                ''')
                
                cursor.execute('''
                    INSERT INTO sections (course_id, title, order_number) VALUES
                    (1, 'Getting Started', 1),
                    (1, 'React Components', 2),
                    (1, 'State and Props', 3),
                    (2, 'Python Basics', 1),
                    (2, 'Data Structures', 2),
                    (3, 'HTML Fundamentals', 1),
                    (3, 'CSS Styling', 2)
                ''')
                
                cursor.execute('''
                    INSERT INTO lessons (section_id, title, order_number, youtube_url, duration) VALUES
                    (1, 'Course Introduction', 1, 'https://www.youtube.com/watch?v=SqcY0GlETPk', 15),
                    (1, 'Setting Up Environment', 2, 'https://www.youtube.com/watch?v=KeP903xkz9M', 20),
                    (2, 'Your First Component', 1, 'https://www.youtube.com/watch?v=Rh3tobgwhXI', 25),
                    (2, 'Component Properties', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 30),
                    (3, 'Understanding State', 1, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 35),
                    (3, 'Working with Props', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 25),
                    (4, 'Python Installation', 1, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 20),
                    (4, 'Variables and Data Types', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 30),
                    (5, 'Lists and Tuples', 1, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 40),
                    (5, 'Dictionaries', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 35),
                    (6, 'HTML Structure', 1, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 25),
                    (6, 'HTML Elements', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 30),
                    (7, 'CSS Basics', 1, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 35),
                    (7, 'CSS Layouts', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 40)
                ''')
            
            conn.commit()
            conn.close()
    
    # Initialize database on startup
    init_db()
    
    # Import routes
    from routes_sqlite import auth_bp, courses_bp, lessons_bp, enrollment_bp, progress_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(lessons_bp, url_prefix='/api/lessons')
    app.register_blueprint(enrollment_bp, url_prefix='/api/enrollment')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    
    # Root endpoint
    @app.route('/')
    def index():
        return jsonify({'message': 'LMS API Server is running in production mode!'})
    
    # Health check endpoint
    @app.route('/health')
    def health_check():
        return jsonify({
            'status': 'healthy',
            'database': 'connected',
            'version': '1.0.0'
        })
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return jsonify({'error': 'Not found'}), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({'error': 'Internal server error'}), 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)
