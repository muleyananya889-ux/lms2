import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Use SQLite for development
    SQLALCHEMY_DATABASE_URI = 'sqlite:///lms_database.db'
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-change-in-production')
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'jwt-secret-key-change-in-production')
    JWT_ACCESS_TOKEN_EXPIRES = 3600  # 1 hour
    
    # YouTube API settings (optional for future features)
    YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY', '')
