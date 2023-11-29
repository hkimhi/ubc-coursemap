from config import *
import sqlite3

# 1. Retrieve all courses from the database
# 2. For each course, add self as post-req for each of its prereqs
# 3. Batch update back to database
def fill_postreqs():
    # Create SQLite connection and cursor
    connection = sqlite3.connect(DATABASE_FILE_PATH)
    cursor = connection.cursor()

    # Fetch all courses
    cursor.execute(f"SELECT name, prereqs FROM {DATABASE_TABLE_NAME}")
    all_courses = cursor.fetchall()

    # Dictionary to store postreqs for each course
    postreqs_dict = {course[0]: [] for course in all_courses}

    # Go through each course and fill in the post-reqs list for all of its prereqs
    for course in all_courses:
        course_name, prereqs = course

        for prereq in prereqs.split(', '):
            # non empty strings are truthy
            if prereq and prereq in postreqs_dict:
                postreqs_dict[prereq].append(course_name)

    # Update the postreqs field in the database
    for course_name, postreqs in postreqs_dict.items():
        postreqs_str = ', '.join(postreqs)
        cursor.execute(f"UPDATE {DATABASE_TABLE_NAME} SET postreqs = ? WHERE name = ?",
                       (postreqs_str, course_name))
    
    # Commit postreqs to the database
    connection.commit()

    # Close the SQLite connection
    connection.close()

    print("Finished filling post-reqs!")

if __name__ == '__main__':
    fill_postreqs()
