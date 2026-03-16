import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { BookOpen, User, LogOut, Menu, X, Home, BarChart3 } from 'lucide-react';

const Navbar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
    setIsMobileMenuOpen(false);
  };

  const isActivePath = (path) => {
    return location.pathname === path;
  };

  return (
    <nav className="bg-white shadow-lg sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* Logo and main nav */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-2">
              <BookOpen className="h-8 w-8 text-primary-600" />
              <span className="text-xl font-bold text-gray-900">LMS</span>
            </Link>

            {/* Desktop navigation */}
            <div className="hidden md:flex items-center space-x-8 ml-10">
              <Link
                to="/"
                className={`text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                  isActivePath('/') ? 'text-primary-600 bg-primary-50' : ''
                }`}
              >
                <Home className="inline h-4 w-4 mr-1" />
                Home
              </Link>
              
              {isAuthenticated && (
                <>
                  <Link
                    to="/courses"
                    className={`text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActivePath('/courses') ? 'text-primary-600 bg-primary-50' : ''
                    }`}
                  >
                    <BookOpen className="inline h-4 w-4 mr-1" />
                    Courses
                  </Link>
                  
                  <Link
                    to="/dashboard"
                    className={`text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors ${
                      isActivePath('/dashboard') ? 'text-primary-600 bg-primary-50' : ''
                    }`}
                  >
                    <BarChart3 className="inline h-4 w-4 mr-1" />
                    Dashboard
                  </Link>
                </>
              )}
            </div>
          </div>

          {/* User menu */}
          <div className="hidden md:flex items-center space-x-4">
            {isAuthenticated ? (
              <div className="flex items-center space-x-3">
                <span className="text-gray-700 text-sm">
                  Welcome, {user?.name}
                </span>
                <span className="px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                  {user?.role}
                </span>
                <button
                  onClick={handleLogout}
                  className="flex items-center space-x-1 text-gray-600 hover:text-red-600 transition-colors"
                >
                  <LogOut className="h-4 w-4" />
                  <span className="text-sm">Logout</span>
                </button>
              </div>
            ) : (
              <div className="flex items-center space-x-3">
                <Link
                  to="/login"
                  className="text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-sm font-medium transition-colors"
                >
                  Login
                </Link>
                <Link
                  to="/signup"
                  className="bg-primary-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-primary-700 transition-colors"
                >
                  Sign Up
                </Link>
              </div>
            )}
          </div>

          {/* Mobile menu button */}
          <div className="md:hidden flex items-center">
            <button
              onClick={() => setIsMobileMenuOpen(!isMobileMenuOpen)}
              className="text-gray-700 hover:text-primary-600 p-2"
            >
              {isMobileMenuOpen ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
            </button>
          </div>
        </div>

        {/* Mobile navigation menu */}
        {isMobileMenuOpen && (
          <div className="md:hidden">
            <div className="px-2 pt-2 pb-3 space-y-1 sm:px-3">
              <Link
                to="/"
                className={`block text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium ${
                  isActivePath('/') ? 'text-primary-600 bg-primary-50' : ''
                }`}
                onClick={() => setIsMobileMenuOpen(false)}
              >
                <Home className="inline h-4 w-4 mr-2" />
                Home
              </Link>
              
              {isAuthenticated && (
                <>
                  <Link
                    to="/courses"
                    className={`block text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium ${
                      isActivePath('/courses') ? 'text-primary-600 bg-primary-50' : ''
                    }`}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <BookOpen className="inline h-4 w-4 mr-2" />
                    Courses
                  </Link>
                  
                  <Link
                    to="/dashboard"
                    className={`block text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium ${
                      isActivePath('/dashboard') ? 'text-primary-600 bg-primary-50' : ''
                    }`}
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    <BarChart3 className="inline h-4 w-4 mr-2" />
                    Dashboard
                  </Link>
                </>
              )}
              
              {isAuthenticated ? (
                <div className="border-t border-gray-200 pt-4">
                  <div className="px-3 py-2">
                    <div className="text-base font-medium text-gray-800">{user?.name}</div>
                    <div className="text-sm text-gray-500">{user?.email}</div>
                    <span className="inline-block mt-1 px-2 py-1 text-xs font-medium bg-primary-100 text-primary-800 rounded-full">
                      {user?.role}
                    </span>
                  </div>
                  <button
                    onClick={handleLogout}
                    className="block w-full text-left text-gray-700 hover:text-red-600 px-3 py-2 rounded-md text-base font-medium"
                  >
                    <LogOut className="inline h-4 w-4 mr-2" />
                    Logout
                  </button>
                </div>
              ) : (
                <div className="border-t border-gray-200 pt-4">
                  <Link
                    to="/login"
                    className="block text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Login
                  </Link>
                  <Link
                    to="/signup"
                    className="block text-gray-700 hover:text-primary-600 px-3 py-2 rounded-md text-base font-medium"
                    onClick={() => setIsMobileMenuOpen(false)}
                  >
                    Sign Up
                  </Link>
                </div>
              )}
            </div>
          </div>
        )}
      </div>
    </nav>
  );
};

export default Navbar;
