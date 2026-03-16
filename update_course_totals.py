#!/usr/bin/env python3
"""
Update course totals (lessons and duration)
"""

import sqlite3

def update_course_totals():
    conn = sqlite3.connect('lms_database.db')
    cursor = conn.cursor()
    
    # Update course totals based on actual lessons
    courses_data = [
        (1, 6, 150),  # Introduction to React - 6 lessons, 150 minutes total
        (2, 4, 110),  # Python for Beginners - 4 lessons, 110 minutes total  
        (3, 4, 130)   # Web Development Fundamentals - 4 lessons, 130 minutes total
    ]
    
    for course_id, total_lessons, total_duration in courses_data:
        cursor.execute("""
            UPDATE courses 
            SET total_lessons = ?, total_duration = ?
            WHERE course_id = ?
        """, (total_lessons, total_duration, course_id))
        
        # Get course title for display
        cursor.execute("SELECT title FROM courses WHERE course_id = ?", (course_id,))
        title = cursor.fetchone()[0]
        print(f"✅ Updated totals for: {title} ({total_lessons} lessons, {total_duration} min)")
    
    conn.commit()
    
    # Verify the updates
    cursor.execute("SELECT course_id, title, total_lessons, total_duration FROM courses")
    courses = cursor.fetchall()
    
    print("\n📚 Updated Course Totals:")
    print("=" * 50)
    for course in courses:
        print(f"ID: {course[0]}")
        print(f"Title: {course[1]}")
        print(f"Lessons: {course[2]}")
        print(f"Duration: {course[3]} minutes")
        print("-" * 30)
    
    conn.close()
    print("\n✅ Course totals updated successfully!")

if __name__ == "__main__":
    update_course_totals()
