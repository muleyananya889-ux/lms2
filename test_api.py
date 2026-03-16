#!/usr/bin/env python3
"""
Test API endpoints
"""

import requests
import json

def test_backend():
    print("🧪 Testing LMS Backend API...")
    
    try:
        # Test root endpoint
        response = requests.get('http://localhost:5000/', timeout=5)
        print(f"✅ Root endpoint: {response.status_code}")
        print(f"   Response: {response.json()}")
        
        # Test courses endpoint
        response = requests.get('http://localhost:5000/api/courses', timeout=5)
        print(f"✅ Courses endpoint: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            courses = data.get('courses', [])
            print(f"   Found {len(courses)} courses")
            for course in courses[:2]:  # Show first 2 courses
                print(f"   - {course['title']}")
        else:
            print(f"   Error: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_backend()
