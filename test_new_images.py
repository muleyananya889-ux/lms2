#!/usr/bin/env python3
"""
Test new course images
"""

import requests

def test_new_course_images():
    print("🖼️ Testing New Course Images...")
    
    # New course image URLs from database
    course_images = [
        ("Introduction to React", "https://picsum.photos/400/200?random=1"),
        ("Python for Beginners", "https://picsum.photos/400/200?random=2"),
        ("Web Development Fundamentals", "https://picsum.photos/400/200?random=3")
    ]
    
    print("=" * 60)
    
    for title, image_url in course_images:
        try:
            response = requests.head(image_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {title}")
                print(f"   Status: {response.status_code}")
                print(f"   URL: {image_url}")
                print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            else:
                print(f"❌ {title} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {title} - Error: {e}")
        print("-" * 40)
    
    print("\n🎯 All images should now be working!")
    print("📱 Access the app at: http://localhost:3000")
    print("🔄 You may need to refresh the browser to see updated images")

if __name__ == "__main__":
    test_new_course_images()
