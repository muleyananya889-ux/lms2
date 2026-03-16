import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import { lessonsAPI, progressAPI, coursesAPI } from '../services/api';
import { 
  Play, 
  Pause, 
  ChevronLeft, 
  ChevronRight, 
  CheckCircle, 
  Circle,
  Loader,
  Clock,
  BookOpen,
  ArrowLeft
} from 'lucide-react';

const LearningPage = () => {
  const { courseId, lessonId } = useParams();
  const navigate = useNavigate();
  
  const [lesson, setLesson] = useState(null);
  const [course, setCourse] = useState(null);
  const [lessons, setLessons] = useState([]);
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [markingComplete, setMarkingComplete] = useState(false);

  useEffect(() => {
    if (courseId && lessonId) {
      fetchLessonData();
      fetchCourseProgress();
    }
  }, [courseId, lessonId]);

  const fetchLessonData = async () => {
    try {
      setLoading(true);
      const [lessonResponse, courseResponse, lessonsResponse] = await Promise.all([
        lessonsAPI.getById(lessonId),
        coursesAPI.getById(courseId),
        lessonsAPI.getCourseLessons(courseId)
      ]);
      
      setLesson(lessonResponse.data.lesson);
      setCourse(courseResponse.data.course);
      
      // Flatten all lessons from all sections
      const allLessons = [];
      lessonsResponse.data.sections.forEach(section => {
        section.lessons.forEach(lesson => {
          allLessons.push({
            ...lesson,
            sectionTitle: section.title
          });
        });
      });
      setLessons(allLessons);
    } catch (err) {
      setError('Failed to load lesson content');
      console.error('Error fetching lesson data:', err);
    } finally {
      setLoading(false);
    }
  };

  const fetchCourseProgress = async () => {
    try {
      const response = await progressAPI.getCourseProgress(courseId);
      setProgress(response.data.progress);
    } catch (err) {
      console.error('Error fetching progress:', err);
    }
  };

  const markLessonComplete = async () => {
    try {
      setMarkingComplete(true);
      await progressAPI.update({
        course_id: parseInt(courseId),
        lesson_id: parseInt(lessonId),
        status: 'completed'
      });
      
      // Update local progress
      setProgress(prev => ({
        ...prev,
        completed_lessons: (prev?.completed_lessons || 0) + 1,
        percentage: Math.round(((prev?.completed_lessons || 0) + 1) / (prev?.total_lessons || 1) * 100)
      }));
      
      // Auto-navigate to next lesson
      if (lesson.navigation.next) {
        navigate(`/learn/${courseId}/${lesson.navigation.next.lesson_id}`);
      }
    } catch (err) {
      console.error('Error marking lesson complete:', err);
    } finally {
      setMarkingComplete(false);
    }
  };

  const navigateToLesson = (lessonId) => {
    navigate(`/learn/${courseId}/${lessonId}`);
  };

  const formatDuration = (minutes) => {
    if (!minutes) return '0 min';
    const hours = Math.floor(minutes / 60);
    const mins = minutes % 60;
    return hours > 0 ? `${hours}h ${mins}m` : `${mins}m`;
  };

  const getYouTubeEmbedUrl = (url) => {
    if (!url) return '';
    
    const videoId = url.includes('youtube.com/watch?v=') 
      ? url.split('v=')[1].split('&')[0]
      : url.includes('youtu.be/') 
      ? url.split('youtu.be/')[1].split('?')[0]
      : '';
    
    return videoId ? `https://www.youtube.com/embed/${videoId}` : '';
  };

  const getLessonStatus = (lessonId) => {
    if (!progress) return 'not_started';
    // This would need to be enhanced to check specific lesson progress
    return 'not_started';
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <Loader className="h-12 w-12 text-primary-600 animate-spin mx-auto mb-4" />
          <p className="text-gray-600">Loading lesson...</p>
        </div>
      </div>
    );
  }

  if (error || !lesson) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <p className="text-red-600 mb-4">{error || 'Lesson not found'}</p>
          <button
            onClick={() => navigate(`/courses/${courseId}`)}
            className="bg-primary-600 text-white px-4 py-2 rounded-md hover:bg-primary-700"
          >
            Back to Course
          </button>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Header */}
      <div className="bg-white shadow-sm border-b">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            <div className="flex items-center space-x-4">
              <button
                onClick={() => navigate(`/courses/${courseId}`)}
                className="flex items-center text-gray-600 hover:text-gray-900"
              >
                <ArrowLeft className="h-5 w-5 mr-2" />
                Back to Course
              </button>
              <div className="h-6 w-px bg-gray-300"></div>
              <h1 className="text-lg font-medium text-gray-900">{course?.title}</h1>
            </div>
            
            {/* Progress Bar */}
            {progress && (
              <div className="flex items-center space-x-4">
                <div className="text-sm text-gray-600">
                  {progress.completed_lessons} / {progress.total_lessons} completed
                </div>
                <div className="w-32 bg-gray-200 rounded-full h-2">
                  <div 
                    className="bg-green-500 h-2 rounded-full transition-all duration-300"
                    style={{ width: `${progress.percentage}%` }}
                  ></div>
                </div>
                <span className="text-sm font-medium text-gray-900">
                  {progress.percentage}%
                </span>
              </div>
            )}
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
          {/* Lesson List Sidebar */}
          <div className="lg:col-span-1">
            <div className="bg-white rounded-lg shadow-sm">
              <div className="p-4 border-b">
                <h2 className="font-semibold text-gray-900">Course Content</h2>
              </div>
              <div className="max-h-96 overflow-y-auto">
                {lessons.map((lessonItem, index) => {
                  const status = getLessonStatus(lessonItem.id);
                  const isCurrentLesson = lessonItem.id === parseInt(lessonId);
                  
                  return (
                    <div
                      key={lessonItem.id}
                      className={`p-4 border-b hover:bg-gray-50 cursor-pointer transition-colors ${
                        isCurrentLesson ? 'bg-primary-50 border-l-4 border-primary-600' : ''
                      }`}
                      onClick={() => navigateToLesson(lessonItem.id)}
                    >
                      <div className="flex items-start space-x-3">
                        <div className="flex-shrink-0 mt-1">
                          {status === 'completed' ? (
                            <CheckCircle className="h-5 w-5 text-green-500" />
                          ) : (
                            <Circle className="h-5 w-5 text-gray-400" />
                          )}
                        </div>
                        <div className="flex-1 min-w-0">
                          <h3 className={`text-sm font-medium ${
                            isCurrentLesson ? 'text-primary-600' : 'text-gray-900'
                          }`}>
                            {lessonItem.title}
                          </h3>
                          <p className="text-xs text-gray-500 mt-1">
                            {lessonItem.sectionTitle}
                          </p>
                          <div className="flex items-center text-xs text-gray-500 mt-1">
                            <Clock className="h-3 w-3 mr-1" />
                            {formatDuration(lessonItem.duration)}
                          </div>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            </div>
          </div>

          {/* Main Content Area */}
          <div className="lg:col-span-3">
            {/* Video Player */}
            <div className="bg-white rounded-lg shadow-sm mb-6">
              <div className="aspect-w-16 aspect-h-9">
                <div className="youtube-player">
                  <iframe
                    src={getYouTubeEmbedUrl(lesson.youtube_url)}
                    title={lesson.title}
                    allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture"
                    allowFullScreen
                    className="w-full h-full"
                  ></iframe>
                </div>
              </div>
              
              {/* Lesson Info */}
              <div className="p-6">
                <h2 className="text-2xl font-bold text-gray-900 mb-4">
                  {lesson.title}
                </h2>
                
                <div className="flex items-center justify-between mb-6">
                  <div className="flex items-center space-x-4 text-sm text-gray-600">
                    <div className="flex items-center">
                      <Clock className="h-4 w-4 mr-1" />
                      <span>{formatDuration(lesson.duration)}</span>
                    </div>
                    <div className="flex items-center">
                      <BookOpen className="h-4 w-4 mr-1" />
                      <span>{lesson.section?.title}</span>
                    </div>
                  </div>
                  
                  <button
                    onClick={markLessonComplete}
                    disabled={markingComplete}
                    className="flex items-center px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700 disabled:opacity-50 disabled:cursor-not-allowed"
                  >
                    {markingComplete ? (
                      <Loader className="h-4 w-4 animate-spin mr-2" />
                    ) : (
                      <CheckCircle className="h-4 w-4 mr-2" />
                    )}
                    Mark as Complete
                  </button>
                </div>

                {/* Navigation */}
                <div className="flex items-center justify-between pt-4 border-t">
                  <div>
                    {lesson.navigation.previous && (
                      <button
                        onClick={() => navigateToLesson(lesson.navigation.previous.lesson_id)}
                        className="flex items-center text-gray-600 hover:text-gray-900"
                      >
                        <ChevronLeft className="h-4 w-4 mr-1" />
                        Previous: {lesson.navigation.previous.title}
                      </button>
                    )}
                  </div>
                  
                  <div>
                    {lesson.navigation.next && (
                      <button
                        onClick={() => navigateToLesson(lesson.navigation.next.lesson_id)}
                        className="flex items-center text-gray-600 hover:text-gray-900"
                      >
                        Next: {lesson.navigation.next.title}
                        <ChevronRight className="h-4 w-4 ml-1" />
                      </button>
                    )}
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default LearningPage;
