// Mock data for Vercel deployment without backend
window.mockCourses = [
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

// Mock API responses
window.mockAPI = {
  courses: {
    getAll: () => Promise.resolve({ data: { courses: window.mockCourses } }),
    getById: (id) => {
      const course = window.mockCourses.find(c => c.id === parseInt(id));
      return Promise.resolve({ data: { course } });
    }
  },
  auth: {
    login: (credentials) => {
      // Mock login
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
