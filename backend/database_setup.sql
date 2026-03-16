-- Learning Management System Database Schema

-- Create database
CREATE DATABASE IF NOT EXISTS lms_database;
USE lms_database;

-- Users table
CREATE TABLE users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role ENUM('student', 'instructor', 'admin') DEFAULT 'student',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);

-- Courses table
CREATE TABLE courses (
    course_id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    description TEXT,
    thumbnail VARCHAR(255),
    category VARCHAR(100),
    instructor_id INT,
    total_lessons INT DEFAULT 0,
    total_duration INT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (instructor_id) REFERENCES users(user_id) ON DELETE SET NULL
);

-- Sections table
CREATE TABLE sections (
    section_id INT AUTO_INCREMENT PRIMARY KEY,
    course_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    order_number INT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_section_order (course_id, order_number)
);

-- Lessons table
CREATE TABLE lessons (
    lesson_id INT AUTO_INCREMENT PRIMARY KEY,
    section_id INT NOT NULL,
    title VARCHAR(255) NOT NULL,
    order_number INT NOT NULL,
    youtube_url VARCHAR(255) NOT NULL,
    duration INT DEFAULT 0, -- duration in minutes
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (section_id) REFERENCES sections(section_id) ON DELETE CASCADE,
    UNIQUE KEY unique_lesson_order (section_id, order_number)
);

-- Enrollments table
CREATE TABLE enrollments (
    enrollment_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    enrollment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    UNIQUE KEY unique_enrollment (user_id, course_id)
);

-- Progress table
CREATE TABLE progress (
    progress_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    course_id INT NOT NULL,
    lesson_id INT NOT NULL,
    status ENUM('completed', 'in_progress') DEFAULT 'in_progress',
    last_watched TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(course_id) ON DELETE CASCADE,
    FOREIGN KEY (lesson_id) REFERENCES lessons(lesson_id) ON DELETE CASCADE,
    UNIQUE KEY unique_progress (user_id, lesson_id)
);

-- Insert sample data
-- Sample users
INSERT INTO users (name, email, password, role) VALUES
('John Doe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'instructor'),
('Jane Smith', 'jane@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'student'),
('Admin User', 'admin@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/LewdBPj6ukx.LFvO6', 'admin');

-- Sample courses
INSERT INTO courses (title, description, thumbnail, category, instructor_id) VALUES
('Introduction to React', 'Learn the basics of React.js including components, props, state, and hooks.', 'https://via.placeholder.com/300x200?text=React+Course', 'Programming', 1),
('Python for Beginners', 'Start your programming journey with Python fundamentals and basic concepts.', 'https://via.placeholder.com/300x200?text=Python+Course', 'Programming', 1),
('Web Development Fundamentals', 'Master HTML, CSS, and JavaScript to build modern websites.', 'https://via.placeholder.com/300x200?text=Web+Dev', 'Web Development', 1);

-- Sample sections
INSERT INTO sections (course_id, title, order_number) VALUES
(1, 'Getting Started', 1),
(1, 'React Components', 2),
(1, 'State and Props', 3),
(2, 'Python Basics', 1),
(2, 'Data Structures', 2),
(3, 'HTML Fundamentals', 1),
(3, 'CSS Styling', 2);

-- Sample lessons
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
(7, 'CSS Layouts', 2, 'https://www.youtube.com/watch?v=QH1-xDF2P2E', 40);

-- Update course totals
UPDATE courses SET 
    total_lessons = (SELECT COUNT(*) FROM lessons WHERE section_id IN (SELECT section_id FROM sections WHERE course_id = courses.course_id)),
    total_duration = (SELECT SUM(duration) FROM lessons WHERE section_id IN (SELECT section_id FROM sections WHERE course_id = courses.course_id));

-- Sample enrollments
INSERT INTO enrollments (user_id, course_id) VALUES
(2, 1),
(2, 2);
