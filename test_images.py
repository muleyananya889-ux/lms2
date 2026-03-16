#!/usr/bin/env python3
"""
Test if course images are accessible
"""

import requests

def test_course_images():
    print("🖼️ Testing Course Images Accessibility...")
    
    # Course image URLs
    course_images = [
        ("Introduction to React", "https://images.unsplash.com/photo-1633356122545-f7210b5b7c5c?w=400&h=200&fit=crop"),
        ("Python for Beginners", "https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=200&fit=crop"),
        ("Web Development Fundamentals", "https://images.unsplash.com/photo-1467232004584-a241f8b4d9e4?w=400&h=200&fit=crop")
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
    
    print("\n🎯 Note: Images should now be visible in the course listing!")
    print("📱 Access the app at: http://localhost:3000")

if __name__ == "__main__":
    test_course_images()
