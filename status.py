#!/usr/bin/env python3
"""
Simple LMS Status Display
"""

import subprocess
import time
import os
from datetime import datetime

def get_server_status():
    """Get current server status"""
    print("=" * 60)
    print("🎓 LEARNING MANAGEMENT SYSTEM - STATUS")
    print("=" * 60)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # Check servers
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True)
        lines = result.stdout.split('\n')
        
        frontend_running = any(':3000' in line and 'LISTENING' in line for line in lines)
        backend_running = any(':5000' in line and 'LISTENING' in line for line in lines)
        
        print(f"🌐 Frontend Server (http://localhost:3000)")
        print(f"   Status: {'✅ RUNNING' if frontend_running else '❌ STOPPED'}")
        print()
        
        print(f"🔧 Backend Server (http://localhost:5000)")
        print(f"   Status: {'✅ RUNNING' if backend_running else '❌ STOPPED'}")
        print()
        
        if frontend_running and backend_running:
            print("🎉 LMS Application is fully operational!")
            print()
            print("📱 Access URLs:")
            print("   🏠 Main App: http://localhost:3000")
            print("   🔧 API: http://localhost:5000/api/courses")
            print()
            print("🔐 Test Users:")
            print("   👨‍🎓 Student: jane@example.com / password123")
            print("   👨‍🏫 Instructor: john@example.com / password123")
            print("   👨‍💼 Admin: admin@example.com / password123")
        else:
            print("❌ Some services are not running")
            
    except Exception as e:
        print(f"Error checking status: {e}")
    
    print("=" * 60)

if __name__ == "__main__":
    get_server_status()
