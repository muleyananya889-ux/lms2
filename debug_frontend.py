#!/usr/bin/env python3
"""
Debug frontend-backend connection
"""

import requests
import json
import time

def test_api_endpoints():
    print("🔍 Debugging Frontend-Backend Connection...")
    
    base_url = "http://localhost:5000"
    
    # Test endpoints that frontend is trying to access
    endpoints = [
        "/",
        "/api/courses",
        "/api/courses/",
        "/api/auth/me"
    ]
    
    print("=" * 60)
    
    for endpoint in endpoints:
        url = base_url + endpoint
        try:
            print(f"Testing: {url}")
            response = requests.get(url, timeout=5)
            print(f"✅ Status: {response.status_code}")
            
            if response.status_code == 200:
                try:
                    data = response.json()
                    if endpoint == "/api/courses" or endpoint == "/api/courses/":
                        courses = data.get('courses', [])
                        print(f"   Found {len(courses)} courses")
                        if courses:
                            print(f"   First course: {courses[0]['title']}")
                    else:
                        print(f"   Response: {data}")
                except:
                    print(f"   Response: {response.text[:100]}")
            else:
                print(f"   Error: {response.text}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
        
        print("-" * 40)
    
    print("\n🎯 Testing with CORS headers...")
    headers = {
        'Origin': 'http://localhost:3000',
        'Access-Control-Request-Method': 'GET',
        'Access-Control-Request-Headers': 'Content-Type,Authorization'
    }
    
    try:
        response = requests.options('http://localhost:5000/api/courses', headers=headers, timeout=5)
        print(f"✅ OPTIONS Status: {response.status_code}")
        print(f"   CORS Headers: {dict(response.headers)}")
    except Exception as e:
        print(f"❌ OPTIONS Error: {e}")

if __name__ == "__main__":
    test_api_endpoints()
