#!/usr/bin/env python3
"""
Fix course images with guaranteed working URLs
"""

import sqlite3

def fix_course_images():
    conn = sqlite3.connect('lms_database.db')
    cursor = conn.cursor()
    
    # Use guaranteed working image URLs
    course_updates = [
        (1, 'https://picsum.photos/400/200?random=1'),  # React course
        (2, 'https://picsum.photos/400/200?random=2'),  # Python course  
        (3, 'https://picsum.photos/400/200?random=3')   # Web Dev course
    ]
    
    for course_id, thumbnail_url in course_updates:
        cursor.execute("""
            UPDATE courses 
            SET thumbnail = ? 
            WHERE course_id = ?
        """, (thumbnail_url, course_id))
        
        # Get course title for display
        cursor.execute("SELECT title FROM courses WHERE course_id = ?", (course_id,))
        title = cursor.fetchone()[0]
        print(f"✅ Fixed thumbnail for: {title}")
    
    conn.commit()
    
    # Verify the updates
    cursor.execute("SELECT course_id, title, thumbnail FROM courses")
    courses = cursor.fetchall()
    
    print("\n📚 Fixed Course Images:")
    print("=" * 50)
    for course in courses:
        print(f"ID: {course[0]}")
        print(f"Title: {course[1]}")
        print(f"Thumbnail: {course[2]}")
        print("-" * 30)
    
    conn.close()
    print("\n✅ All course images fixed with working URLs!")

if __name__ == "__main__":
    fix_course_images()
