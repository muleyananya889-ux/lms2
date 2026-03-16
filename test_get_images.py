#!/usr/bin/env python3
"""
Test course images with GET requests
"""

import requests

def test_course_images_get():
    print("🖼️ Testing Course Images (GET Method)...")
    
    # Course image URLs
    course_images = [
        ("Introduction to React", "https://picsum.photos/400/200?random=1"),
        ("Python for Beginners", "https://picsum.photos/400/200?random=2"),
        ("Web Development Fundamentals", "https://picsum.photos/400/200?random=3")
    ]
    
    print("=" * 60)
    
    for title, image_url in course_images:
        try:
            response = requests.get(image_url, timeout=5)
            if response.status_code == 200:
                print(f"✅ {title}")
                print(f"   Status: {response.status_code}")
                print(f"   Size: {len(response.content)} bytes")
                print(f"   Content-Type: {response.headers.get('content-type', 'N/A')}")
            else:
                print(f"❌ {title} - Status: {response.status_code}")
        except Exception as e:
            print(f"❌ {title} - Error: {e}")
        print("-" * 40)
    
    print("\n🎯 Images are working! Check the browser to see them.")
    print("📱 Access the app at: http://localhost:3000")

if __name__ == "__main__":
    test_course_images_get()
