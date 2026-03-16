#!/usr/bin/env python3
"""
Test detailed course data including images
"""

import requests
import json

def test_courses_with_images():
    print("🧪 Testing LMS Courses with Images...")
    
    try:
        response = requests.get('http://localhost:5000/api/courses', timeout=5)
        if response.status_code == 200:
            data = response.json()
            courses = data.get('courses', [])
            
            print(f"✅ Found {len(courses)} courses:")
            print("=" * 60)
            
            for i, course in enumerate(courses, 1):
                print(f"\n📚 Course {i}:")
                print(f"   ID: {course['id']}")
                print(f"   Title: {course['title']}")
                print(f"   Category: {course['category']}")
                print(f"   Instructor: {course['instructor_name']}")
                print(f"   Lessons: {course['total_lessons']}")
                print(f"   Duration: {course['total_duration']} min")
                print(f"   Thumbnail: {course['thumbnail']}")
                print(f"   Enrollments: {course['enrollment_count']}")
                print("   " + "-" * 50)
        else:
            print(f"❌ Error: {response.status_code}")
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    test_courses_with_images()
