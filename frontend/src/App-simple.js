import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider, useAuth } from './context/AuthContext';
import Navbar from './components/Navbar';
import Login from './pages/Login';
import Signup from './pages/Signup';
import Dashboard from './pages/Dashboard';
import CourseList from './pages/CourseList';
import CourseDetails from './pages/CourseDetails';
import LearningPage from './pages/LearningPage';
import './index.css';

// Mock data for standalone deployment
const mockCourses = [
  {
    id: 1,
    title: "Introduction to React",
    description: "Learn the basics of React.js including components, props, state, and hooks.",
    thumbnail: "https://picsum.photos/400/200?random=1",
    category: "Programming",
    instructor_name: "John Doe",
    total_lessons: 6,
    total_duration: 150,
    enrollment_count: 0,
    created_at: new Date().toISOString()
  },
  {
    id: 2,
    title: "Python for Beginners",
    description: "Start your programming journey with Python fundamentals and basic concepts.",
    thumbnail: "https://picsum.photos/400/200?random=2",
    category: "Programming",
    instructor_name: "John Doe",
    total_lessons: 4,
    total_duration: 110,
    enrollment_count: 0,
    created_at: new Date().toISOString()
  },
  {
    id: 3,
    title: "Web Development Fundamentals",
    description: "Master HTML, CSS, and JavaScript to build modern websites.",
    thumbnail: "https://picsum.photos/400/200?random=3",
    category: "Web Development",
    instructor_name: "John Doe",
    total_lessons: 4,
    total_duration: 130,
    enrollment_count: 0,
    created_at: new Date().toISOString()
  }
];

// Mock API
const mockAPI = {
  courses: {
    getAll: () => Promise.resolve({ data: { courses: mockCourses } }),
    getById: (id) => {
      const course = mockCourses.find(c => c.id === parseInt(id));
      return Promise.resolve({ data: { course } });
    }
  },
  auth: {
    login: (credentials) => {
      if (credentials.email === 'jane@example.com' && credentials.password === 'password123') {
        return Promise.resolve({ 
          data: { 
            message: 'Login successful',
            user: { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'student' },
            access_token: 'mock-token'
          }
        });
      }
      return Promise.reject({ response: { status: 401, data: { error: 'Invalid credentials' } } });
    },
    signup: (userData) => Promise.resolve({
      data: { 
        message: 'User created successfully',
        user: { id: 4, name: userData.name, email: userData.email, role: userData.role },
        access_token: 'mock-token'
      }
    }),
    getCurrentUser: () => Promise.resolve({
      data: { user: { id: 2, name: 'Jane Smith', email: 'jane@example.com', role: 'student' } }
    })
  }
};

// Protected Route Component
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated, loading } = useAuth();
  
  if (loading) {
    return (
      <div className="min-h-screen flex items-center justify-center">
        <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-600"></div>
      </div>
    );
  }
  
  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }
  
  return children;
};

// Main App Component
function App() {
  return (
    <AuthProvider>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Navbar />
          <main className="container mx-auto px-4 py-8">
            <Routes>
              <Route path="/" element={<CourseList />} />
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="/courses/:id" element={<CourseDetails />} />
              <Route 
                path="/learning/:courseId/:lessonId" 
                element={
                  <ProtectedRoute>
                    <LearningPage />
                  </ProtectedRoute>
                } 
              />
              <Route 
                path="/dashboard" 
                element={
                  <ProtectedRoute>
                    <Dashboard />
                  </ProtectedRoute>
                } 
              />
            </Routes>
          </main>
        </div>
      </Router>
    </AuthProvider>
  );
}

export default App;
