import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { coursesAPI, enrollmentAPI } from '../services/api';
import { 
  BookOpen, 
  Clock, 
  Users, 
  Star, 
  ArrowLeft, 
  Play, 
  CheckCircle, 
  Loader,
  User,
  Calendar
} from 'lucide-react';

const CourseDetails = () => {
  const { id } = useParams();
  const { user, isAuthenticated } = useAuth();
  const navigate = useNavigate();
  
  const [course, setCourse] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [enrolling, setEnrolling] = useState(false);
  const [isEnrolled, setIsEnrolled] = useState(false);

  useEffect(() => {
    fetchCourseDetails();
    if (isAuthenticated) {
      checkEnrollment();
    }
  }, [id, isAuthenticated]);

  const fetchCourseDetails = async () => {
    try {
      setLoading(true);
      const response = await coursesAPI.getById(id);
      setCourse(response.data.course);
    } catch (err) {
      setError('Failed to fetch course details');
      console.error('Error fetching course details:', err);
    } finally {
      setLoading(false);
    }
  };

  const checkEnrollment = async () => {
    try {
      const response = await enrollmentAPI.checkEnrollment(id);
      setIsEnrolled(response.data.enrolled);
    } catch (err) {
      console.error('Error checking enrollment:', err);
    }
  };

  const handleEnroll = async () => {
    if (!isAuthenticated) {
      navigate('/login');
      return;
    }

    try {
      setEnrolling(true);
      await enrollmentAPI.enroll(id);
      setIsEnrolled(true);
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to enroll in course');
    } finally {
      setEnrolling(false);
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '0 min';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="h-12 w-12 text-primary-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading course details...</p>
        </div>
      </div>
    );
  }

  if (error || !course) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Course not found'}</p>
          <button
            onClick={() => navigate('/courses')}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
          >
            Back to Courses
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Course Header */}
      <div className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate('/courses')}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Courses
              </button>
            </div>
          </div>
        </div>
      </div>

      {/* Course Content */}
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
          {/* Main Content */}
          <div className="lg:col-span-2">
            {/* Course Title and Description */}
            <div className="bg-white rounded-lg shadow-sm p-6 mb-6">
              <div className="flex items-start justify-between mb-4">
                <div className="flex-1">
                  <h1 className="text-3xl font-bold text-gray-900 mb-4">
                    {course.title}
                  </h1>
                  <div className="flex items-center space-x-4 text-sm text-gray-600 mb-4">
                    <div className="flex items-center">
                      <User className="h-4 w-4 mr-1" />
                      <span>{course.instructor_name}</span>
                    </div>
                    <div className="flex items-center">
                      <Calendar className="h-4 w-4 mr-1" />
                      <span>Created {new Date(course.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
              </div>

              <p className="text-gray-700 leading-relaxed mb-6">
                {course.description}
              </p>

              {/* Course Stats */}
              <div className="grid grid-cols-3 gap-4 py-4 border-t border-gray-200">
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {course.total_lessons}
                  </div>
                  <div className="text-sm text-gray-600">Lessons</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {formatDuration(course.total_duration)}
                  </div>
                  <div className="text-sm text-gray-600">Duration</div>
                </div>
                <div className="text-center">
                  <div className="text-2xl font-bold text-primary-600">
                    {course.category}
                  </div>
                  <div className="text-sm text-gray-600">Category</div>
                </div>
              </div>
            </div>

            {/* Course Sections and Lessons */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h2 className="text-xl font-semibold text-gray-900 mb-6">
                Course Content
              </h2>
              {course.sections && course.sections.length > 0 ? (
                <div className="space-y-6">
                  {course.sections.map((section, sectionIndex) => (
                    <div key={section.id} className="border border-gray-200 rounded-lg">
                      <div className="bg-gray-50 px-4 py-3 border-b border-gray-200">
                        <h3 className="font-medium text-gray-900">
                          {sectionIndex + 1}. {section.title}
                        </h3>
                      </div>
                      <div className="divide-y divide-gray-200">
                        {section.lessons && section.lessons.length > 0 ? (
                          section.lessons.map((lesson, lessonIndex) => (
                            <div
                              key={lesson.id}
                              className="px-4 py-3 hover:bg-gray-50 transition-colors"
                            >
                              <div className="flex items-center justify-between">
                                <div className="flex items-center space-x-3">
                                  <div className="flex items-center justify-center w-8 h-8 bg-primary-100 text-primary-600 rounded-full text-sm font-medium">
                                    {lessonIndex + 1}
                                  </div>
                                  <div>
                                    <h4 className="font-medium text-gray-900">
                                      {lesson.title}
                                    </h4>
                                    <div className="flex items-center space-x-2 text-sm text-gray-500">
                                      <Clock className="h-3 w-3" />
                                      <span>{formatDuration(lesson.duration)}</span>
                                    </div>
                                  </div>
                                </div>
                                {isEnrolled && (
                                  <Link
                                    to={`/learn/${course.id}/${lesson.id}`}
                                    className="flex items-center text-primary-600 hover:text-primary-700"
                                  >
                                    <Play className="h-4 w-4 mr-1" />
                                    Watch
                                  </Link>
                                )}
                              </div>
                            </div>
                          ))
                        ) : (
                          <div className="px-4 py-3 text-gray-500 text-sm">
                            No lessons available in this section
                          </div>
                        )}
                      </div>
                    </div>
                  ))}
                </div>
              ) : (
                <div className="text-center py-8 text-gray-500">
                  <BookOpen className="h-12 w-12 mx-auto mb-4 text-gray-400" />
                  <p>No course content available yet</p>
                </div>
              )}
            </div>
          </div>

          {/* Sidebar */}
          <div className="lg:col-span-1">
            {/* Course Thumbnail */}
            <div className="bg-white rounded-lg shadow-sm overflow-hidden mb-6">
              <div className="relative h-48 bg-gray-200">
                {course.thumbnail ? (
                  <img
                    src={course.thumbnail}
                    alt={course.title}
                    className="w-full h-full object-cover"
                  />
                ) : (
                  <div className="w-full h-full flex items-center justify-center">
                    <BookOpen className="h-16 w-16 text-gray-400" />
                  </div>
                )}
              </div>
              
              <div className="p-6">
                {/* Enroll Button */}
                {isEnrolled ? (
                  <div className="space-y-3">
                    <div className="flex items-center justify-center text-green-600 mb-4">
                      <CheckCircle className="h-6 w-6 mr-2" />
                      <span className="font-medium">Enrolled</span>
                    </div>
                    {course.sections && course.sections.length > 0 && course.sections[0].lessons && course.sections[0].lessons.length > 0 && (
                      <Link
                        to={`/learn/${course.id}/${course.sections[0].lessons[0].id}`}
                        className="block w-full bg-primary-600 text-white text-center py-3 px-4 rounded-md hover:bg-primary-700 transition-colors"
                      >
                        Start Learning
                      </Link>
                    )}
                  </div>
                ) : (
                  <button
                    onClick={handleEnroll}
                    disabled={enrolling}
                    className="w-full bg-primary-600 text-white py-3 px-4 rounded-md hover:bg-primary-700 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {enrolling ? (
                      <div className="flex items-center justify-center">
                        <Loader className="h-5 w-5 animate-spin mr-2" />
                        Enrolling...
                      </div>
                    ) : (
                      'Enroll Now'
                    )}
                  </button>
                )}

                {!isAuthenticated && (
                  <p className="text-sm text-gray-600 text-center mt-3">
                    <Link to="/login" className="text-primary-600 hover:text-primary-700">
                      Login
                    </Link>
                    {' '}to enroll in this course
                  </p>
                )}
              </div>
            </div>

            {/* Course Info */}
            <div className="bg-white rounded-lg shadow-sm p-6">
              <h3 className="font-semibold text-gray-900 mb-4">Course Information</h3>
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Instructor</span>
                  <span className="font-medium">{course.instructor_name}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Category</span>
                  <span className="font-medium">{course.category}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Lessons</span>
                  <span className="font-medium">{course.total_lessons}</span>
                </div>
                <div className="flex items-center justify-between">
                  <span className="text-gray-600">Duration</span>
                  <span className="font-medium">{formatDuration(course.total_duration)}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default CourseDetails;
