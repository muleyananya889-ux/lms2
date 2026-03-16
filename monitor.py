#!/usr/bin/env python3
"""
LMS Application Monitor
Shows real-time status of backend and frontend servers
"""

import requests
import time
import subprocess
import sys
import os
from datetime import datetime

def check_backend():
    """Check if backend is running"""
    try:
        response = requests.get('http://localhost:5000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def check_frontend():
    """Check if frontend is running"""
    try:
        response = requests.get('http://localhost:3000/', timeout=5)
        return response.status_code == 200
    except:
        return False

def get_backend_status():
    """Get detailed backend status"""
    try:
        response = requests.get('http://localhost:5000/api/courses', timeout=5)
        if response.status_code == 200:
            data = response.json()
            return f"✅ API Working - {len(data.get('courses', []))} courses available"
        else:
            return f"❌ API Error - Status {response.status_code}"
    except Exception as e:
        return f"❌ Connection Failed - {str(e)}"

def display_status():
    """Display current server status"""
    os.system('cls' if os.name == 'nt' else 'clear')
    
    print("=" * 60)
    print("🎓 LEARNING MANAGEMENT SYSTEM - MONITOR")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Backend Status
    backend_running = check_backend()
    print(f"🔧 Backend Server (http://localhost:5000)")
    print(f"   Status: {'✅ RUNNING' if backend_running else '❌ STOPPED'}")
    if backend_running:
        print(f"   Details: {get_backend_status()}")
    print()
    
    # Frontend Status
    frontend_running = check_frontend()
    print(f"🌐 Frontend Server (http://localhost:3000)")
    print(f"   Status: {'✅ RUNNING' if frontend_running else '❌ STOPPED'}")
    print()
    
    # Access URLs
    print("📱 Access URLs:")
    print("   🏠 Main App: http://localhost:3000")
    print("   🔧 API Docs: http://localhost:5000/api/courses")
    print()
    
    # Test Users
    print("🔐 Test Users:")
    print("   👨‍🎓 Student: jane@example.com / password123")
    print("   👨‍🏫 Instructor: john@example.com / password123")
    print("   👨‍💼 Admin: admin@example.com / password123")
    print()
    
    print("=" * 60)
    print("Press Ctrl+C to stop monitoring")
    print("=" * 60)

def main():
    print("🚀 Starting LMS Monitor...")
    
    try:
        while True:
            display_status()
            time.sleep(5)
    except KeyboardInterrupt:
        print("\n🛑 Monitor stopped")
        sys.exit(0)

if __name__ == "__main__":
    main()
