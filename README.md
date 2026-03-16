# Learning Management System (LMS)

A full-stack Learning Management System built with React.js frontend and Python Flask backend, featuring YouTube video integration, course management, and progress tracking.

## 🚀 Features

### Core Features
- **User Authentication**: Secure JWT-based authentication with role-based access (Student, Instructor, Admin)
- **Course Management**: Create, view, and manage courses with sections and lessons
- **Video Learning**: Integrated YouTube video player for lesson content
- **Progress Tracking**: Track lesson completion and course progress
- **Enrollment System**: Student enrollment management
- **Responsive Design**: Modern UI built with Tailwind CSS

### User Roles
- **Students**: Browse courses, enroll, watch lessons, track progress
- **Instructors**: Create and manage courses, upload lessons
- **Admin**: Full system access and user management

## 🛠 Tech Stack

### Frontend
- **React.js** - Modern JavaScript framework
- **React Router** - Client-side routing
- **Axios** - HTTP client for API calls
- **Tailwind CSS** - Utility-first CSS framework
- **Lucide React** - Icon library

### Backend
- **Python Flask** - Web framework
- **Flask-JWT-Extended** - JWT authentication
- **PyMySQL** - MySQL database connector
- **bcrypt** - Password hashing
- **Flask-CORS** - Cross-origin resource sharing

### Database
- **MySQL** - Relational database

## 📋 Prerequisites

- Python 3.8+
- Node.js 14+
- MySQL 5.7+ or 8.0+
- npm or yarn

## 🚀 Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd lms2
```

### 2. Backend Setup

#### Install Dependencies
```bash
cd backend
pip install -r requirements.txt
```

#### Database Setup
```bash
# Create MySQL database
mysql -u root -p
CREATE DATABASE lms_database;

# Import database schema
mysql -u root -p lms_database < database_setup.sql
```

#### Environment Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your database credentials
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_mysql_password
MYSQL_DB=lms_database
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key
```

#### Start Backend Server
```bash
python app.py
```

The backend will run on `http://localhost:5000`

### 3. Frontend Setup

#### Install Dependencies
```bash
cd frontend
npm install
```

#### Start Frontend Development Server
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## 📁 Project Structure

```
lms2/
├── backend/
│   ├── app.py                 # Main Flask application
│   ├── config.py              # Configuration settings
│   ├── database_setup.sql     # Database schema and sample data
│   ├── requirements.txt       # Python dependencies
│   ├── .env.example          # Environment variables template
│   └── routes/
│       ├── auth.py           # Authentication routes
│       ├── courses.py        # Course management routes
│       ├── lessons.py        # Lesson management routes
│       ├── enrollment.py     # Enrollment routes
│       └── progress.py       # Progress tracking routes
├── frontend/
│   ├── public/
│   │   └── index.html        # HTML template
│   ├── src/
│   │   ├── components/
│   │   │   └── Navbar.js     # Navigation component
│   │   ├── context/
│   │   │   └── AuthContext.js # Authentication context
│   │   ├── pages/
│   │   │   ├── Login.js      # Login page
│   │   │   ├── Signup.js     # Signup page
│   │   │   ├── CourseList.js # Course listing page
│   │   │   ├── CourseDetails.js # Course details page
│   │   │   ├── LearningPage.js # Video learning interface
│   │   │   └── Dashboard.js  # User dashboard
│   │   ├── services/
│   │   │   └── api.js        # API service layer
│   │   ├── App.js            # Main React component
│   │   └── index.js          # React entry point
│   ├── package.json          # Node.js dependencies
│   └── tailwind.config.js    # Tailwind CSS configuration
└── README.md                 # This file
```

## 🔐 Default Users

The database setup includes sample users for testing:

| Email | Password | Role |
|-------|----------|------|
| john@example.com | password123 | instructor |
| jane@example.com | password123 | student |
| admin@example.com | password123 | admin |

## 📚 API Endpoints

### Authentication
- `POST /api/auth/login` - User login
- `POST /api/auth/signup` - User registration
- `GET /api/auth/me` - Get current user

### Courses
- `GET /api/courses` - Get all courses
- `GET /api/courses/:id` - Get course details
- `POST /api/courses` - Create new course (instructor/admin)
- `PUT /api/courses/:id` - Update course (instructor/admin)

### Lessons
- `GET /api/lessons/courses/:course_id/lessons` - Get course lessons
- `GET /api/lessons/:lesson_id` - Get lesson details
- `POST /api/lessons` - Create new lesson (instructor/admin)
- `PUT /api/lessons/:lesson_id` - Update lesson (instructor/admin)

### Enrollment
- `POST /api/enrollment/enroll` - Enroll in course
- `GET /api/enrollment/user/:user_id` - Get user enrollments
- `GET /api/enrollment/check/:course_id` - Check enrollment status
- `DELETE /api/enrollment/unenroll` - Unenroll from course

### Progress
- `POST /api/progress/update` - Update lesson progress
- `GET /api/progress/:course_id` - Get course progress
- `GET /api/progress/dashboard/:user_id` - Get user dashboard data
- `DELETE /api/progress/reset/:course_id` - Reset course progress

## 🎯 Usage Guide

### For Students
1. **Sign Up**: Create a student account
2. **Browse Courses**: Explore available courses
3. **Enroll**: Enroll in courses of interest
4. **Learn**: Watch video lessons and track progress
5. **Dashboard**: Monitor learning progress and achievements

### For Instructors
1. **Sign Up**: Create an instructor account
2. **Create Courses**: Design course structure with sections and lessons
3. **Add Lessons**: Upload YouTube video URLs for each lesson
4. **Manage Content**: Update course information and lesson details
5. **Track Students**: Monitor student enrollment and progress

### For Admins
1. **Full Access**: Manage all aspects of the system
2. **User Management**: Oversee user accounts and roles
3. **Content Oversight**: Review and manage all courses
4. **System Analytics**: Monitor platform usage and statistics

## 🔧 Configuration

### Backend Configuration (.env)
```env
# Database settings
MYSQL_HOST=localhost
MYSQL_USER=root
MYSQL_PASSWORD=your_password
MYSQL_DB=lms_database

# Security keys (change these in production!)
SECRET_KEY=your-super-secret-key
JWT_SECRET_KEY=your-jwt-secret-key

# YouTube API (optional)
YOUTUBE_API_KEY=your_youtube_api_key
```

### Frontend Configuration
The frontend automatically connects to the backend at `http://localhost:5000`. To change this, update the `API_BASE_URL` in `src/services/api.js`.

## 🐛 Troubleshooting

### Common Issues

1. **Database Connection Error**
   - Ensure MySQL is running
   - Check database credentials in `.env`
   - Verify database was created and schema imported

2. **CORS Errors**
   - Backend includes CORS configuration for `localhost:3000`
   - For different ports, update CORS origins in `app.py`

3. **JWT Token Issues**
   - Tokens expire after 1 hour by default
   - Clear browser localStorage to reset authentication

4. **YouTube Video Not Loading**
   - Ensure YouTube URL format is correct
   - Check if video is public/unlisted (not private)
   - Verify YouTube embed permissions

### Development Tips

- Use browser DevTools to inspect API requests
- Check backend console for error messages
- Verify database state with MySQL client
- Test API endpoints with tools like Postman

## 🚀 Deployment

### Backend Deployment
1. Set up production MySQL database
2. Configure production environment variables
3. Use WSGI server (Gunicorn) for production
4. Set up reverse proxy (Nginx)

### Frontend Deployment
1. Build production bundle: `npm run build`
2. Serve static files with web server
3. Configure API endpoint for production

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License.

## 📞 Support

For support and questions:
- Create an issue in the repository
- Check existing issues for solutions
- Review documentation and troubleshooting section

---

**Happy Learning! 🎓**
