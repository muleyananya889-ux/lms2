import os
from dotenv import load_dotenv

load_dotenv()

class ProductionConfig:
    # Database Configuration
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///lms_database.db')
    
    # Security Keys
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-production-secret-key-change-this')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your-production-jwt-secret-key-change-this')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # Production Settings
    DEBUG = False
    TESTING = False
    
    # CORS Settings for production
    CORS_ORIGINS = ['https://yourdomain.com', 'http://localhost:3000']
    
    # YouTube API settings (optional)
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
