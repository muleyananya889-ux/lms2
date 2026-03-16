import React, { useState } from 'react';
import './index.css';

// Simple working LMS app for Vercel deployment
function App() {
  const [currentPage, setCurrentPage] = useState('courses');
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [selectedCourse, setSelectedCourse] = useState(null);

  // Mock courses data
  const courses = [
    {
      id: 1,
      title: "Introduction to React",
      description: "Learn the basics of React.js including components, props, state, and hooks.",
      thumbnail: "https://picsum.photos/400/200?random=1",
      category: "Programming",
      instructor_name: "John Doe",
      total_lessons: 6,
      total_duration: 150,
      enrollment_count: 0
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
      enrollment_count: 0
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
      enrollment_count: 0
    }
  ];

  // Navigation component
  const Navbar = () => (
    <nav className="bg-white shadow-lg">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          <div className="flex items-center">
            <h1 className="text-2xl font-bold text-indigo-600">🎓 LMS</h1>
          </div>
          <div className="flex items-center space-x-4">
            <button 
              onClick={() => setCurrentPage('courses')}
              className={`px-3 py-2 rounded-md text-sm font-medium ${currentPage === 'courses' ? 'bg-indigo-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
            >
              Courses
            </button>
            {isLoggedIn && (
              <button 
                onClick={() => setCurrentPage('dashboard')}
                className={`px-3 py-2 rounded-md text-sm font-medium ${currentPage === 'dashboard' ? 'bg-indigo-600 text-white' : 'text-gray-700 hover:bg-gray-100'}`}
              >
                Dashboard
              </button>
            )}
            {isLoggedIn ? (
              <button 
                onClick={() => setIsLoggedIn(false)}
                className="px-3 py-2 rounded-md text-sm font-medium bg-red-600 text-white hover:bg-red-700"
              >
                Logout
              </button>
            ) : (
              <button 
                onClick={() => setCurrentPage('login')}
                className="px-3 py-2 rounded-md text-sm font-medium bg-indigo-600 text-white hover:bg-indigo-700"
              >
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </nav>
  );

  // Course list component
  const CourseList = () => (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      {courses.map(course => (
        <div key={course.id} className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
          <img 
            src={course.thumbnail} 
            alt={course.title}
            className="w-full h-48 object-cover"
          />
          <div className="p-6">
            <div className="text-sm text-indigo-600 font-semibold mb-2">{course.category}</div>
            <h3 className="text-xl font-bold text-gray-900 mb-2">{course.title}</h3>
            <p className="text-gray-600 mb-4">{course.description}</p>
            <div className="flex justify-between items-center text-sm text-gray-500 mb-4">
              <span>👨‍🏫 {course.instructor_name}</span>
              <span>⏱️ {course.total_duration} min</span>
            </div>
            <div className="flex justify-between items-center">
              <span className="text-sm text-gray-500">📚 {course.total_lessons} lessons</span>
              <button 
                onClick={() => {
                  setSelectedCourse(course);
                  setCurrentPage('course-detail');
                }}
                className="px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
              >
                View Course
              </button>
            </div>
          </div>
        </div>
      ))}
    </div>
  );

  // Course detail component
  const CourseDetail = () => {
    if (!selectedCourse) return null;
    
    return (
      <div className="max-w-4xl mx-auto">
        <button 
          onClick={() => setCurrentPage('courses')}
          className="mb-6 px-4 py-2 bg-gray-200 text-gray-700 rounded-md hover:bg-gray-300 transition-colors"
        >
          ← Back to Courses
        </button>
        
        <div className="bg-white rounded-lg shadow-lg overflow-hidden">
          <img 
            src={selectedCourse.thumbnail} 
            alt={selectedCourse.title}
            className="w-full h-64 object-cover"
          />
          <div className="p-8">
            <div className="text-sm text-indigo-600 font-semibold mb-2">{selectedCourse.category}</div>
            <h1 className="text-3xl font-bold text-gray-900 mb-4">{selectedCourse.title}</h1>
            <p className="text-lg text-gray-600 mb-6">{selectedCourse.description}</p>
            
            <div className="grid grid-cols-3 gap-4 mb-8">
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-indigo-600">{selectedCourse.total_lessons}</div>
                <div className="text-sm text-gray-600">Lessons</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-indigo-600">{selectedCourse.total_duration}</div>
                <div className="text-sm text-gray-600">Minutes</div>
              </div>
              <div className="bg-gray-50 p-4 rounded-lg text-center">
                <div className="text-2xl font-bold text-indigo-600">{selectedCourse.enrollment_count}</div>
                <div className="text-sm text-gray-600">Students</div>
              </div>
            </div>
            
            <div className="mb-6">
              <h2 className="text-xl font-bold text-gray-900 mb-4">Course Instructor</h2>
              <div className="flex items-center space-x-4">
                <div className="w-12 h-12 bg-indigo-600 rounded-full flex items-center justify-center text-white font-bold">
                  JD
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{selectedCourse.instructor_name}</div>
                  <div className="text-sm text-gray-600">Expert Instructor</div>
                </div>
              </div>
            </div>
            
            <div className="flex space-x-4">
              <button 
                onClick={() => {
                  if (!isLoggedIn) {
                    setCurrentPage('login');
                  } else {
                    alert('Enrolled successfully!');
                  }
                }}
                className="flex-1 px-6 py-3 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
              >
                {isLoggedIn ? 'Enroll Now' : 'Login to Enroll'}
              </button>
              <button 
                onClick={() => {
                  if (isLoggedIn) {
                    alert('Starting course...');
                  } else {
                    setCurrentPage('login');
                  }
                }}
                className="flex-1 px-6 py-3 bg-green-600 text-white rounded-md hover:bg-green-700 transition-colors"
              >
                {isLoggedIn ? 'Start Learning' : 'Login to Start'}
              </button>
            </div>
          </div>
        </div>
      </div>
    );
  };

  // Login component
  const Login = () => {
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    
    const handleSubmit = (e) => {
      e.preventDefault();
      // Mock login
      if (email && password) {
        setIsLoggedIn(true);
        setCurrentPage('courses');
        alert('Login successful!');
      }
    };
    
    return (
      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Login to LMS</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter your password"
                required
              />
            </div>
            
            <button
              type="submit"
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
            >
              Login
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Don't have an account?{' '}
              <button 
                onClick={() => setCurrentPage('signup')}
                className="text-indigo-600 hover:text-indigo-800 font-medium"
              >
                Sign up
              </button>
            </p>
          </div>
          
          <div className="mt-6 p-4 bg-gray-50 rounded-md">
            <p className="text-sm text-gray-600 font-medium mb-2">Test Users:</p>
            <p className="text-xs text-gray-500">Email: jane@example.com</p>
            <p className="text-xs text-gray-500">Password: password123</p>
          </div>
        </div>
      </div>
    );
  };

  // Signup component
  const Signup = () => {
    const [name, setName] = useState('');
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [role, setRole] = useState('student');
    
    const handleSubmit = (e) => {
      e.preventDefault();
      // Mock signup
      if (name && email && password) {
        setIsLoggedIn(true);
        setCurrentPage('courses');
        alert('Signup successful!');
      }
    };
    
    return (
      <div className="max-w-md mx-auto">
        <div className="bg-white rounded-lg shadow-lg p-8">
          <h2 className="text-2xl font-bold text-gray-900 mb-6">Sign Up for LMS</h2>
          
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Name</label>
              <input
                type="text"
                value={name}
                onChange={(e) => setName(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter your name"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Email</label>
              <input
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter your email"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Password</label>
              <input
                type="password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
                placeholder="Enter your password"
                required
              />
            </div>
            
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">Role</label>
              <select
                value={role}
                onChange={(e) => setRole(e.target.value)}
                className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-indigo-500"
              >
                <option value="student">Student</option>
                <option value="instructor">Instructor</option>
                <option value="admin">Admin</option>
              </select>
            </div>
            
            <button
              type="submit"
              className="w-full px-4 py-2 bg-indigo-600 text-white rounded-md hover:bg-indigo-700 transition-colors"
            >
              Sign Up
            </button>
          </form>
          
          <div className="mt-6 text-center">
            <p className="text-sm text-gray-600">
              Already have an account?{' '}
              <button 
                onClick={() => setCurrentPage('login')}
                className="text-indigo-600 hover:text-indigo-800 font-medium"
              >
                Login
              </button>
            </p>
          </div>
        </div>
      </div>
    );
  };

  // Dashboard component
  const Dashboard = () => (
    <div className="max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold text-gray-900 mb-8">Welcome to your Dashboard</h1>
      
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-indigo-600 mb-2">3</div>
          <div className="text-sm text-gray-600">Enrolled Courses</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-green-600 mb-2">12</div>
          <div className="text-sm text-gray-600">Completed Lessons</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-yellow-600 mb-2">5.5</div>
          <div className="text-sm text-gray-600">Hours Learned</div>
        </div>
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-2xl font-bold text-purple-600 mb-2">85%</div>
          <div className="text-sm text-gray-600">Progress</div>
        </div>
      </div>
      
      <div className="bg-white rounded-lg shadow p-6">
        <h2 className="text-xl font-bold text-gray-900 mb-4">Recent Activity</h2>
        <div className="space-y-3">
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div>
              <div className="font-medium text-gray-900">Introduction to React</div>
              <div className="text-sm text-gray-600">Completed lesson 3</div>
            </div>
            <div className="text-sm text-gray-500">2 hours ago</div>
          </div>
          <div className="flex items-center justify-between p-3 bg-gray-50 rounded">
            <div>
              <div className="font-medium text-gray-900">Python for Beginners</div>
              <div class="text-sm text-gray-600">Started course</div>
            </div>
            <div className="text-sm text-gray-500">1 day ago</div>
          </div>
        </div>
      </div>
    </div>
  );

  // Main render
  return (
    <div className="min-h-screen bg-gray-50">
      <Navbar />
      <main className="container mx-auto px-4 py-8">
        {currentPage === 'courses' && <CourseList />}
        {currentPage === 'course-detail' && <CourseDetail />}
        {currentPage === 'login' && <Login />}
        {currentPage === 'signup' && <Signup />}
        {currentPage === 'dashboard' && <Dashboard />}
      </main>
    </div>
  );
}

export default App;
