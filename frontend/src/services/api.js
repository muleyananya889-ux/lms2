import axios from 'axios';

// Use environment-specific API URL
const API_BASE_URL = process.env.REACT_APP_API_URL || '/api';

// Create axios instance with default config
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Response interceptor to handle errors and fallback to mock data
api.interceptors.response.use(
  (response) => response,
  (error) => {
    // Fallback to mock data if backend is not available
    if (error.code === 'ECONNREFUSED' || error.code === 'ERR_NETWORK' || !error.response) {
      console.log('Backend not available, using mock data');

      // Return mock data for different endpoints
      if (error.config.url.includes('/courses')) {
        if (error.config.method === 'get' && !error.config.url.includes('/courses/')) {
          return Promise.resolve({ data: { courses: window.mockCourses || [] } });
        }
        if (error.config.method === 'get' && error.config.url.match(/\/courses\/\d+/)) {
          const id = error.config.url.split('/').pop();
          const course = (window.mockCourses || []).find(c => c.id === parseInt(id));
          return Promise.resolve({ data: { course } });
        }
      }

      if (error.config.url.includes('/auth/login')) {
        return window.mockAPI.auth.login(error.config.data);
      }

      if (error.config.url.includes('/auth/signup')) {
        return window.mockAPI.auth.signup(error.config.data);
      }

      if (error.config.url.includes('/auth/me')) {
        return window.mockAPI.auth.getCurrentUser();
      }
    }

    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('access_token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  login: (credentials) => api.post('/auth/login', credentials),
  signup: (userData) => api.post('/auth/signup', userData),
  getCurrentUser: () => api.get('/auth/me'),
};

// Courses API
export const coursesAPI = {
  getAll: () => api.get('/courses'),
  getById: (id) => api.get(`/courses/${id}`),
  create: (courseData) => api.post('/courses', courseData),
  update: (id, courseData) => api.put(`/courses/${id}`, courseData),
};

// Lessons API
export const lessonsAPI = {
  getCourseLessons: (courseId) => api.get(`/lessons/courses/${courseId}/lessons`),
  getById: (id) => api.get(`/lessons/${id}`),
  create: (lessonData) => api.post('/lessons', lessonData),
  update: (id, lessonData) => api.put(`/lessons/${id}`, lessonData),
};

// Enrollment API
export const enrollmentAPI = {
  enroll: (courseId) => api.post('/enrollment/enroll', { course_id: courseId }),
  unenroll: (courseId) => api.delete('/enrollment/unenroll', { data: { course_id: courseId } }),
  getUserEnrollments: (userId) => api.get(`/enrollment/user/${userId}`),
  getCourseStudents: (courseId) => api.get(`/enrollment/course/${courseId}/students`),
  checkEnrollment: (courseId) => api.get(`/enrollment/check/${courseId}`),
};

// Progress API
export const progressAPI = {
  update: (progressData) => api.post('/progress/update', progressData),
  getCourseProgress: (courseId) => api.get(`/progress/${courseId}`),
  getLessonProgress: (lessonId) => api.get(`/progress/lesson/${lessonId}`),
  getUserDashboard: (userId) => api.get(`/progress/dashboard/${userId}`),
  resetCourse: (courseId) => api.delete(`/progress/reset/${courseId}`),
};

export default api;
