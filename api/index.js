// Vercel Serverless Function for Backend API
const express = require('express');
const cors = require('cors');
const sqlite3 = require('sqlite3').verbose();

const app = express();

// Enable CORS
app.use(cors({
  origin: true,
  credentials: true
}));

// Parse JSON
app.use(express.json());

// Database connection
const db = new sqlite3.Database('./lms_database.db');

// Initialize database
db.serialize(() => {
  // Create tables
  db.run(`CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL,
    role TEXT DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )`);

  db.run(`CREATE TABLE IF NOT EXISTS courses (
    course_id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    thumbnail TEXT,
    category TEXT,
    instructor_id INTEGER,
    total_lessons INTEGER DEFAULT 0,
    total_duration INTEGER DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
  )`);

  // Insert sample data if empty
  db.get("SELECT COUNT(*) as count FROM courses", (err, row) => {
    if (row.count === 0) {
      const courses = [
        ['Introduction to React', 'Learn the basics of React.js including components, props, state, and hooks.', 'https://picsum.photos/400/200?random=1', 'Programming', 1, 6, 150],
        ['Python for Beginners', 'Start your programming journey with Python fundamentals and basic concepts.', 'https://picsum.photos/400/200?random=2', 'Programming', 1, 4, 110],
        ['Web Development Fundamentals', 'Master HTML, CSS, and JavaScript to build modern websites.', 'https://picsum.photos/400/200?random=3', 'Web Development', 1, 4, 130]
      ];

      courses.forEach(course => {
        db.run("INSERT INTO courses (title, description, thumbnail, category, instructor_id, total_lessons, total_duration) VALUES (?, ?, ?, ?, ?, ?, ?)", course);
      });
    }
  });
});

// API Routes
app.get('/api/courses', (req, res) => {
  db.all("SELECT * FROM courses", (err, rows) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    
    const courses = rows.map(course => ({
      id: course.course_id,
      title: course.title,
      description: course.description,
      thumbnail: course.thumbnail,
      category: course.category,
      instructor_name: 'John Doe',
      total_lessons: course.total_lessons,
      total_duration: course.total_duration,
      enrollment_count: 0,
      created_at: course.created_at
    }));
    
    res.json({ courses });
  });
});

app.get('/api/courses/:id', (req, res) => {
  const courseId = req.params.id;
  
  db.get("SELECT * FROM courses WHERE course_id = ?", [courseId], (err, row) => {
    if (err) {
      res.status(500).json({ error: err.message });
      return;
    }
    
    if (!row) {
      res.status(404).json({ error: 'Course not found' });
      return;
    }
    
    const course = {
      id: row.course_id,
      title: row.title,
      description: row.description,
      thumbnail: row.thumbnail,
      category: row.category,
      instructor_name: 'John Doe',
      total_lessons: row.total_lessons,
      total_duration: row.total_duration,
      sections: [],
      created_at: row.created_at
    };
    
    res.json({ course });
  });
});

// Health check
app.get('/api/health', (req, res) => {
  res.json({ status: 'healthy', database: 'connected' });
});

// Root endpoint
app.get('/', (req, res) => {
  res.json({ message: 'LMS API Server is running on Vercel!' });
});

// Export for Vercel
module.exports = app;
