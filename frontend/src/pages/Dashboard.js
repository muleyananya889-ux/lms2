import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { progressAPI, enrollmentAPI } from '../services/api';
import { 
  BookOpen, 
  Clock, 
  TrendingUp, 
  Award, 
  Play, 
  Loader,
  BarChart3,
  Users,
  Calendar,
  Target
} from 'lucide-react';

const Dashboard = () => {
  const { user } = useAuth();
  const [dashboardData, setDashboardData] = useState(null);
  const [enrollments, setEnrollments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    if (user) {
      fetchDashboardData();
      fetchEnrollments();
    }
  }, [user]);

  const fetchDashboardData = async () => {
    try {
      const response = await progressAPI.getUserDashboard(user.id);
      setDashboardData(response.data);
    } catch (err) {
      console.error('Error fetching dashboard data:', err);
    }
  };

  const fetchEnrollments = async () => {
    try {
      const response = await enrollmentAPI.getUserEnrollments(user.id);
      setEnrollments(response.data.enrollments);
    } catch (err) {
      console.error('Error fetching enrollments:', err);
    } finally {
      setLoading(false);
    }
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '0 min';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getProgressColor = (percentage) => {
    if (percentage === 100) return 'bg-green-500';
    if (percentage >= 50) return 'bg-blue-500';
    if (percentage >= 25) return 'bg-yellow-500';
    return 'bg-gray-300';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="h-12 w-12 text-primary-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Welcome Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">
            Welcome back, {user?.name}!
          </h1>
          <p className="text-gray-600">
            Continue your learning journey and track your progress
          </p>
        </div>

        {/* Statistics Cards */}
        {dashboardData && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-blue-100 rounded-lg">
                  <BookOpen className="h-6 w-6 text-blue-600" />
                </div>
                <span className="text-2xl font-bold text-gray-900">
                  {dashboardData.statistics.total_enrolled}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium">Enrolled Courses</h3>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-green-100 rounded-lg">
                  <Award className="h-6 w-6 text-green-600" />
                </div>
                <span className="text-2xl font-bold text-gray-900">
                  {dashboardData.statistics.total_completed}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium">Completed Courses</h3>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-purple-100 rounded-lg">
                  <Target className="h-6 w-6 text-purple-600" />
                </div>
                <span className="text-2xl font-bold text-gray-900">
                  {dashboardData.statistics.total_lessons_completed}
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium">Lessons Completed</h3>
            </div>

            <div className="bg-white rounded-lg shadow-sm p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="p-3 bg-orange-100 rounded-lg">
                  <TrendingUp className="h-6 w-6 text-orange-600" />
                </div>
                <span className="text-2xl font-bold text-gray-900">
                  {dashboardData.statistics.overall_progress}%
                </span>
              </div>
              <h3 className="text-gray-600 text-sm font-medium">Overall Progress</h3>
            </div>
          </div>
        )}

        {/* Recent Courses */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
          {/* Enrolled Courses */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b">
              <div className="flex items-center justify-between">
                <h2 className="text-lg font-semibold text-gray-900">My Courses</h2>
                <Link
                  to="/courses"
                  className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                >
                  Browse All
                </Link>
              </div>
            </div>
            
            <div className="p-6">
              {enrollments.length === 0 ? (
                <div className="text-center py-8">
                  <BookOpen className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No courses yet</h3>
                  <p className="text-gray-600 mb-4">Start learning by enrolling in a course</p>
                  <Link
                    to="/courses"
                    className="inline-flex items-center px-4 py-2 bg-primary-600 text-white rounded-md hover:bg-primary-700"
                  >
                    <BookOpen className="h-4 w-4 mr-2" />
                    Browse Courses
                  </Link>
                </div>
              ) : (
                <div className="space-y-4">
                  {enrollments.slice(0, 5).map((enrollment) => (
                    <div key={enrollment.id} className="border border-gray-200 rounded-lg p-4">
                      <div className="flex items-start justify-between mb-3">
                        <div className="flex-1">
                          <h3 className="font-medium text-gray-900 mb-1">
                            {enrollment.course.title}
                          </h3>
                          <p className="text-sm text-gray-600 line-clamp-2">
                            {enrollment.course.description}
                          </p>
                        </div>
                      </div>
                      
                      {/* Progress Bar */}
                      <div className="mb-3">
                        <div className="flex items-center justify-between text-sm text-gray-600 mb-1">
                          <span>{enrollment.progress.completed_lessons} / {enrollment.progress.total_lessons} lessons</span>
                          <span>{enrollment.progress.percentage}%</span>
                        </div>
                        <div className="w-full bg-gray-200 rounded-full h-2">
                          <div 
                            className={`h-2 rounded-full transition-all duration-300 ${getProgressColor(enrollment.progress.percentage)}`}
                            style={{ width: `${enrollment.progress.percentage}%` }}
                          ></div>
                        </div>
                      </div>
                      
                      {/* Action Buttons */}
                      <div className="flex items-center justify-between">
                        <div className="flex items-center text-sm text-gray-500">
                          <Calendar className="h-4 w-4 mr-1" />
                          Enrolled {new Date(enrollment.enrollment_date).toLocaleDateString()}
                        </div>
                        
                        {enrollment.progress.percentage > 0 && (
                          <Link
                            to={`/courses/${enrollment.course.id}`}
                            className="flex items-center text-primary-600 hover:text-primary-700 text-sm font-medium"
                          >
                            <Play className="h-4 w-4 mr-1" />
                            Continue Learning
                          </Link>
                        )}
                      </div>
                    </div>
                  ))}
                  
                  {enrollments.length > 5 && (
                    <div className="text-center pt-4">
                      <Link
                        to="/courses"
                        className="text-primary-600 hover:text-primary-700 text-sm font-medium"
                      >
                        View all courses →
                      </Link>
                    </div>
                  )}
                </div>
              )}
            </div>
          </div>

          {/* Learning Activity */}
          <div className="bg-white rounded-lg shadow-sm">
            <div className="p-6 border-b">
              <h2 className="text-lg font-semibold text-gray-900">Learning Activity</h2>
            </div>
            
            <div className="p-6">
              {enrollments.length === 0 ? (
                <div className="text-center py-8">
                  <BarChart3 className="h-12 w-12 text-gray-400 mx-auto mb-4" />
                  <h3 className="text-lg font-medium text-gray-900 mb-2">No activity yet</h3>
                  <p className="text-gray-600">Start learning to see your progress here</p>
                </div>
              ) : (
                <div className="space-y-4">
                  {/* Overall Progress */}
                  {dashboardData && (
                    <div className="bg-gradient-to-r from-primary-50 to-blue-50 rounded-lg p-4">
                      <div className="flex items-center justify-between mb-2">
                        <h3 className="font-medium text-gray-900">Overall Progress</h3>
                        <span className="text-2xl font-bold text-primary-600">
                          {dashboardData.statistics.overall_progress}%
                        </span>
                      </div>
                      <div className="w-full bg-white rounded-full h-3">
                        <div 
                          className="bg-gradient-to-r from-primary-500 to-blue-500 h-3 rounded-full transition-all duration-500"
                          style={{ width: `${dashboardData.statistics.overall_progress}%` }}
                        ></div>
                      </div>
                    </div>
                  )}
                  
                  {/* Recent Activity */}
                  <div>
                    <h3 className="font-medium text-gray-900 mb-3">Recent Activity</h3>
                    <div className="space-y-3">
                      {enrollments
                        .filter(e => e.progress.percentage > 0)
                        .sort((a, b) => new Date(b.last_activity) - new Date(a.last_activity))
                        .slice(0, 3)
                        .map((enrollment) => (
                          <div key={enrollment.id} className="flex items-center space-x-3">
                            <div className="flex-shrink-0">
                              <div className={`w-2 h-2 rounded-full ${getProgressColor(enrollment.progress.percentage)}`}></div>
                            </div>
                            <div className="flex-1 min-w-0">
                              <p className="text-sm text-gray-900">
                                Progress in <span className="font-medium">{enrollment.course.title}</span>
                              </p>
                              <p className="text-xs text-gray-500">
                                {enrollment.progress.percentage}% completed
                              </p>
                            </div>
                          </div>
                        ))}
                      
                      {enrollments.filter(e => e.progress.percentage > 0).length === 0 && (
                        <p className="text-sm text-gray-500">No recent activity</p>
                      )}
                    </div>
                  </div>
                  
                  {/* Learning Stats */}
                  <div className="grid grid-cols-2 gap-4 pt-4">
                    <div className="text-center">
                      <div className="text-2xl font-bold text-primary-600">
                        {dashboardData?.statistics.total_lessons_completed || 0}
                      </div>
                      <div className="text-sm text-gray-600">Lessons Completed</div>
                    </div>
                    <div className="text-center">
                      <div className="text-2xl font-bold text-green-600">
                        {dashboardData?.statistics.total_completed || 0}
                      </div>
                      <div className="text-sm text-gray-600">Courses Finished</div>
                    </div>
                  </div>
                </div>
              )}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
