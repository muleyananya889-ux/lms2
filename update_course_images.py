#!/usr/bin/env python3
"""
Update course images with proper working URLs
"""

import sqlite3

def update_course_images():
    conn = sqlite3.connect('lms_database.db')
    cursor = conn.cursor()
    
    # Update course thumbnails with proper image URLs
    course_updates = [
        (1, 'Introduction to React', 'https://images.unsplash.com/photo-1633356122545-f7210b5b7c5c?w=400&h=200&fit=crop'),
        (2, 'Python for Beginners', 'https://images.unsplash.com/photo-1526379095098-d400fd0bf935?w=400&h=200&fit=crop'),
        (3, 'Web Development Fundamentals', 'https://images.unsplash.com/photo-1467232004584-a241f8b4d9e4?w=400&h=200&fit=crop')
    ]
    
    for course_id, title, thumbnail_url in course_updates:
        cursor.execute("""
            UPDATE courses 
            SET thumbnail = ? 
            WHERE course_id = ? AND title = ?
        """, (thumbnail_url, course_id, title))
        print(f"✅ Updated thumbnail for: {title}")
    
    conn.commit()
    
    # Verify the updates
    cursor.execute("SELECT course_id, title, thumbnail FROM courses")
    courses = cursor.fetchall()
    
    print("\n📚 Updated Course Images:")
    print("=" * 50)
    for course in courses:
        print(f"ID: {course[0]}")
        print(f"Title: {course[1]}")
        print(f"Thumbnail: {course[2]}")
        print("-" * 30)
    
    conn.close()
    print("\n✅ Course images updated successfully!")

if __name__ == "__main__":
    update_course_images()
