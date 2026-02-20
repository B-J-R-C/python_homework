import sqlite3

# --- Helper Functions to Handle Duplicates and Lookups ---

def add_student(cursor, name, age, major):
    try:
        cursor.execute("INSERT INTO Students (name, age, major) VALUES (?,?,?)", (name, age, major))
        print(f"Added student: {name}")
    except sqlite3.IntegrityError:
        print(f"Student '{name}' is already in the database.")

def add_course(cursor, name, instructor):
    try:
        cursor.execute("INSERT INTO Courses (course_name, instructor_name) VALUES (?,?)", (name, instructor))
        print(f"Added course: {name}")
    except sqlite3.IntegrityError:
        print(f"Course '{name}' is already in the database.")

def enroll_student(cursor, student_name, course_name):
    # 1. Find the Student ID
    cursor.execute("SELECT student_id FROM Students WHERE name = ?", (student_name,))
    student_result = cursor.fetchone()
    
    if not student_result:
        print(f"Error: Could not find student '{student_name}'.")
        return
    student_id = student_result[0]

    # 2. Find the Course ID
    cursor.execute("SELECT course_id FROM Courses WHERE course_name = ?", (course_name,))
    course_result = cursor.fetchone()
    
    if not course_result:
        print(f"Error: Could not find course '{course_name}'.")
        return
    course_id = course_result[0]

    # 3. Check if enrollment already exists (to prevent duplicates)
    cursor.execute("SELECT * FROM Enrollments WHERE student_id = ? AND course_id = ?", (student_id, course_id))
    if cursor.fetchone():
        print(f"Student '{student_name}' is already enrolled in '{course_name}'.")
        return

    # 4. Insert Enrollment
    try:
        cursor.execute("INSERT INTO Enrollments (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
        print(f"Enrolled: {student_name} -> {course_name}")
    except sqlite3.Error as e:
        print(f"Error enrolling {student_name}: {e}")


# --- Main Execution Block ---

# Connect to the database
with sqlite3.connect("../db/school.db") as conn:
    conn.execute("PRAGMA foreign_keys = 1") # Turn on foreign key constraints
    cursor = conn.cursor()

    print("--- Adding Students ---")
    add_student(cursor, 'Alice', 20, 'Computer Science')
    add_student(cursor, 'Bob', 22, 'History')
    add_student(cursor, 'Charlie', 19, 'Biology')

    print("\n--- Adding Courses ---")
    add_course(cursor, 'Math 101', 'Dr. Smith')
    add_course(cursor, 'English 101', 'Ms. Jones')
    add_course(cursor, 'Chemistry 101', 'Dr. Lee')

    print("\n--- Enrolling Students ---")
    enroll_student(cursor, "Alice", "Math 101")
    enroll_student(cursor, "Alice", "Chemistry 101")
    enroll_student(cursor, "Bob", "Math 101")
    enroll_student(cursor, "Bob", "English 101")
    enroll_student(cursor, "Charlie", "English 101")

    # Commit the changes to save them to the file
    conn.commit()
    print("\nTransaction committed. Data saved successfully.")