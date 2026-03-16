from flask import Flask
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from config import Config
import pymysql
from functools import wraps

pymysql.install_as_MySQLdb()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Enable CORS
    CORS(app, origins=["http://localhost:3000"])
    
    # Database connection helper
    def get_db_connection():
        try:
            connection = pymysql.connect(
                host=app.config['MYSQL_HOST'],
                user=app.config['MYSQL_USER'],
                password=app.config['MYSQL_PASSWORD'],
                database=app.config['MYSQL_DB'],
                cursorclass=pymysql.cursors.DictCursor
            )
            return connection
        except Exception as e:
            print(f"Database connection error: {e}")
            return None
    
    # Make database connection available to all routes
    app.get_db_connection = get_db_connection
    
    # Register blueprints
    from routes.auth import auth_bp
    from routes.courses import courses_bp
    from routes.lessons import lessons_bp
    from routes.enrollment import enrollment_bp
    from routes.progress import progress_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(courses_bp, url_prefix='/api/courses')
    app.register_blueprint(lessons_bp, url_prefix='/api/lessons')
    app.register_blueprint(enrollment_bp, url_prefix='/api/enrollment')
    app.register_blueprint(progress_bp, url_prefix='/api/progress')
    
    # Root endpoint
    @app.route('/')
    def index():
        return {'message': 'LMS API Server is running!'}
    
    # Error handlers
    @app.errorhandler(404)
    def not_found(error):
        return {'error': 'Not found'}, 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return {'error': 'Internal server error'}, 500
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, port=5000)
