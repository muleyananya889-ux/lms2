#!/usr/bin/env python3
"""
LMS Application Startup Script
This script starts both the backend and frontend servers
"""

import subprocess
import sys
import os
import time
import webbrowser
from threading import Thread

def start_backend():
    """Start the Flask backend server"""
    print("🚀 Starting backend server...")
    backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Start the SQLite backend
    process = subprocess.Popen([sys.executable, 'app_sqlite.py'], 
                              stdout=subprocess.PIPE, 
                              stderr=subprocess.PIPE)
    return process

def start_frontend():
    """Start the React frontend server"""
    print("🚀 Starting frontend server...")
    frontend_dir = os.path.join(os.path.dirname(__file__), 'frontend')
    
    # Change to frontend directory
    os.chdir(frontend_dir)
    
    # Start npm start
    if sys.platform == "win32":
        process = subprocess.Popen(['npm', 'start'], 
                                  shell=True,
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
    else:
        process = subprocess.Popen(['npm', 'start'], 
                                  stdout=subprocess.PIPE, 
                                  stderr=subprocess.PIPE)
    return process

def main():
    print("🎓 Learning Management System Startup")
    print("=" * 50)
    
    # Check if directories exist
    if not os.path.exists('backend'):
        print("❌ Backend directory not found!")
        return
    
    if not os.path.exists('frontend'):
        print("❌ Frontend directory not found!")
        return
    
    # Start backend
    backend_process = start_backend()
    print("✅ Backend server starting on http://localhost:5000")
    
    # Wait a moment for backend to start
    time.sleep(3)
    
    # Start frontend
    frontend_process = start_frontend()
    print("✅ Frontend server starting on http://localhost:3000")
    
    # Wait for frontend to start
    time.sleep(10)
    
    # Open browser
    print("🌐 Opening application in browser...")
    webbrowser.open('http://localhost:3000')
    
    print("\n🎉 LMS Application is now running!")
    print("📱 Frontend: http://localhost:3000")
    print("🔧 Backend API: http://localhost:5000")
    print("\n🔐 Test Users:")
    print("   Student: jane@example.com / password123")
    print("   Instructor: john@example.com / password123")
    print("   Admin: admin@example.com / password123")
    print("\n⏹️  Press Ctrl+C to stop the servers")
    
    try:
        # Keep script running
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 Stopping servers...")
        backend_process.terminate()
        frontend_process.terminate()
        print("✅ Servers stopped successfully")

if __name__ == "__main__":
    main()
