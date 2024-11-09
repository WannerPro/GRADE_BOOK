"""
Gradebook Management System
A command-line application for managing student grades and academic records.
Author: WANGODA FRANCIS
Student Number: 2400711855
"""

# Import required standard libraries
import json          # For handling JSON data storage
import statistics    # For statistical calculations


# Student identification constants
STUDENT_NAME = "WANGODA FRANCIS"
STUDENT_NUMBER = "2400711855"
REGISTRATION_NUMBER = "24/U/11855/PS"


class Student:
    """
    Class representing a student with their personal details and academic marks.
    Handles individual student data management including marks for different subjects.
    """
    
    def __init__(self, admin_no, name):
        """
        Initialize a new student with their basic information.
        
        Args:
            admin_no (str): Student's administrative number
            name (str): Student's full name
        """
        self.admin_no = admin_no
        self.name = name
        # Initialize default marks as 0 for all subjects
        self.marks = {
            "Maths": 0,
            "SST": 0,
            "English": 0,
            "Science": 0,
        }
        
    def set_marks(self, subject, marks):
        """
        Set marks for a specific subject with validation.
        
        Args:
            subject (str): Subject name
            marks (int): Marks to be set (must be between 0 and 100)
            
        Returns:
            bool: True if marks were set successfully, False if validation fails
        """
        if subject in self.marks and 0 <= marks <= 100:
            self.marks[subject] = marks
            return True
        return False
    
    def get_marks(self, subject):
        """
        Retrieve marks for a specific subject with validation.
        
        Args:
            subject (str): Subject name
            
        Returns:
            int or None: Marks if valid, None if invalid
        """
        return self.marks.get(subject) if 0 <= self.marks.get(subject) <= 100 else None
    
    def edit_marks(self, subject, new_marks):
        """
        Edit existing marks for a subject.
        
        Args:
            subject (str): Subject name
            new_marks (int): New marks to be set
            
        Returns:
            bool or None: True if edit successful, False/None if failed
        """
        return self.set_marks(subject, new_marks) if subject else None


class Gradebook:
    """
    Class managing the entire gradebook system.
    Handles operations like adding/removing students and grade management.
    """
    
    def __init__(self, filename='previous_data.json'):
        """
        Initialize gradebook and load existing data.
        
        Args:
            filename (str): Path to JSON file storing gradebook data
        """
        self.filename = filename
        self.students = {}  # Dictionary to store student objects
        self.load_data()
    
    def load_data(self):
        """
        Load existing student data from JSON file into memory.
        Handles FileNotFoundError if data file doesn't exist.
        """
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                # Create Student objects from JSON data
                for admin_no, info in data.items():
                    student = Student(admin_no, info['name'])
                    student.marks = info["marks"]
                    self.students[admin_no] = student
        except FileNotFoundError:
            print("Error! the file not found")
    
    def save_data(self):
        """
        Save current student data to JSON file.
        Converts student objects to dictionary format for JSON storage.
        """
        data = {admin_no:{"name": student.name,"marks": student.marks} 
                for admin_no, student in self.students.items()}
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    def add_student(self, student):
        """
        Add a new student to the gradebook.
        
        Args:
            student (Student): Student object to add
            
        Returns:
            bool: True if student added successfully, False if already exists
        """
        if student.admin_no not in self.students:
            self.students[student.admin_no] = student
            self.save_data()
            return True
        return False
    
    def get_student(self, admin_no):
        """
        Retrieve a student's information.
        
        Args:
            admin_no (str): Student's administrative number
            
        Returns:
            Student or None: Student object if found, None if not found
        """
        return self.students.get(admin_no)
    
    def delete_student(self, admin_no):
        """
        Remove a student from the gradebook.
        
        Args:
            admin_no (str): Student's administrative number
            
        Returns:
            bool: True if student deleted successfully, False if not found
        """
        if admin_no in self.students:
            del self.students[admin_no]
            self.save_data()
            return True
        return False
    
    def view_statistics(self):
        """
        Calculate and return statistical analysis of grades for all subjects.
        Includes average, max, min, mode, and mode frequency for each subject.
        
        Returns:
            dict: Dictionary containing statistical measures for each subject
        """
        # Initialize dictionary to collect marks for each subject
        subject_marks = {subject: [] for subject in ["Maths", "SST", "English", "Science"]}
        
        # Collect valid marks for each subject from all students
        for student in self.students.values():
            for subject in subject_marks:
                mark = student.get_marks(subject)
                if mark is not None:
                    subject_marks[subject].append(mark)

        # Helper functions for statistical calculations
        def calc_average(marks):
            """Calculate average of marks list"""
            return format(sum(marks) / len(marks), '.4f') if marks else None
        
        def calc_mode_freq(marks):
            """Calculate mode and its frequency from marks list"""
            if not marks:
                return "No mode", "No Frequency"
            mode_value = statistics.mode(marks)
            return mode_value, marks.count(mode_value)
        
        # Calculate statistics for each subject
        grade_stats = {}
        for subject in subject_marks:
            marks = subject_marks[subject]
            mode_value, mode_freq = calc_mode_freq(marks)
            
            stats = {
                f'Average_{subject}': calc_average(marks),
                f'Max_{subject}': max(marks) if marks else None,
                f'Min_{subject}': min(marks) if marks else None,
                f'Mode_{subject}': mode_value,
                f'Mode_Freq_{subject}': mode_freq
            }
            grade_stats.update(stats)
        
        return grade_stats
    
    def view_student_grades(self, admin_no):
        """
        Get all grades for a specific student.
        
        Args:
            admin_no (str): Student's administrative number
            
        Returns:
            dict or None: Dictionary of student's grades if found
        """
        student = self.get_student(admin_no)
        if student:
            return {
                'Maths': student.marks["Maths"],
                'English': student.marks["English"],
                'Science': student.marks["Science"],
                'SST': student.marks["SST"]
            }
        else:
            print("Student does not exist in the system!")

    def print_gradebook(self):
        """
        Get summary of all students in the gradebook.
        
        Returns:
            dict: Dictionary containing total number of students and their details
        """
        return {
            'total_students': len(self.students),
            'student_details': {admin_no: student.name 
                              for admin_no, student in self.students.items()}
        }


def print_menu():
    """Display the main menu options for the gradebook system."""
    print("--------------------Menu--------------------")
    print("1 - Add student")
    print("2 - Delete student, given an admin_no")
    print("3 - View statistics about the grades")
    print("4 - View student grades")
    print("5 - Edit or Enter student grades")
    print("6 - Print Gradebook")
    print("m - Print menu")
    print("c - Clear Screen")
    print("q - Quit system\n")


def main():
    """
    Main function to run the gradebook application.
    Handles user interaction and menu choices.
    """
    # Initialize gradebook
    gradebook = Gradebook()
    
    # Main program loop
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()
        
        # Handle user choices
        if choice == '1':
            # Add new student
            admin_no = input("Enter Admin Number: ").strip()
            name = input("Enter Student Name: ").strip()
            student = Student(admin_no,name)
            if gradebook.add_student(student):
                print(f"Student {name} added successfully.")
            else:
                print(f"Student with Admin Number {admin_no} already exists.")
        
        elif choice == '2':
            # Delete existing student
            admin_no = input("Enter Admin Number to delete: ").strip()
            if gradebook.delete_student(admin_no):
                print(f"Student with Admin Number {admin_no} deleted!")
            else:
                print("Student not found!")

        elif choice == '3':
            # View statistical analysis
            stats = gradebook.view_statistics()
            for stat, value in stats.items():
                print("-"*50)
                print(f"{stat}: {value}")
                print("-"*50)

        elif choice == '4':
            # View individual student grades
            admin_no = input("Enter Admin Number to view grades: ").strip()
            grades = gradebook.view_student_grades(admin_no)
            if grades is not None:
                for key, value in grades.items():
                    print(f"{key}: {value}")
            else:
                print("Student not found.")

        elif choice == '5':
            # Edit student grades
            admin_no = input("Enter Admin Number to edit grades: ").strip()
            student = gradebook.get_student(admin_no)
            if student:
                for subject in ["Maths", "SST", "English", "Science"]:
                    choice = input(f"Edit {subject} marks! (Y/N): ").strip().upper()
                    if choice == 'Y':
                        marks = int(input("Enter new marks (0-100): ").strip())
                        if student.edit_marks(subject, marks):
                            gradebook.save_data()
                            print("Marks updated.")
                            print("-"*50)
                        else:
                            print("Invalid subject marks.")
                    elif choice == 'N' or choice == "":
                        print("Operation cancelled!")
            else:
                print("Student not found!")

        elif choice == '6':
            # Print gradebook summary
            data = gradebook.print_gradebook()
            for key, value in data.items():
                print(f"{key}: {value}")

        elif choice == 'm':
            # Show menu again
            print_menu()

        elif choice == 'c':
            # Clear screen
            print("\033c", end="")

        elif choice == 'q':
            # Save and quit
            gradebook.save_data()
            print("Exiting the system. Goodbye!")
            break
            
        else:
            # Handle invalid input
            print("Invalid choice. Please try again.")


# Entry point of the program
if __name__ == "__main__":
    main()
