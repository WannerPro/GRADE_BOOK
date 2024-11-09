import json
import statistics
import time
import sys

# Student identification constants
STUDENT_NAME = "JOHN DOE"
STUDENT_NUMBER = "290000198"
REGISTRATION_NUMBER = "88/U/0198/PS"


class Student:
    """
    A class to represent a student and their academic records.
    Handles individual student data including admin number, name, and subject marks.
    """
    def __init__(self, admin_no, name):
        """
        Initialize a new student with their basic information and empty marks.
        
        Args:
            admin_no (str): Student's administrative number
            name (str): Student's full name
        """
        self.admin_no = admin_no
        self.name = name
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
            bool: True if marks were set successfully, False otherwise
        """
        if subject in self.marks and 0 <= marks <= 100:
            self.marks[subject] = marks
            return True
        return False
    
    def get_marks(self, subject):
        """
        Retrieve marks for a specific subject.
        
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
    A class to manage the entire gradebook system.
    Handles operations like adding/removing students, managing grades, and generating statistics.
    """
    def __init__(self, filename='previous_data.json'):
        """
        Initialize gradebook with data from a JSON file.
        
        Args:
            filename (str): Path to the JSON file storing gradebook data
        """
        self.filename = filename
        self.students = {}
        self.load_data()
    
    def load_data(self):
        """Load existing student data from JSON file into memory."""
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for admin_no, info in data.items():
                    student = Student(admin_no, info['name'])
                    student.marks = info["marks"]
                    self.students[admin_no] = student
        except FileNotFoundError:
            print("Error! the file not found")
    
    def save_data(self):
        """Save current student data to JSON file."""
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
            bool: True if student added successfully, False if student already exists
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
            Student or None: Student object if found, None otherwise
        """
        return self.students.get(admin_no)
    
    def delete_student(self, admin_no):
        """
        Remove a student from the gradebook.
        
        Args:
            admin_no (str): Student's administrative number
            
        Returns:
            bool: True if student deleted successfully, False if student not found
        """
        if admin_no in self.students:
            del self.students[admin_no]
            self.save_data()
            return True
        return False
    
    def view_statistics(self):
        """
        Calculate and return statistical analysis of grades for all subjects.
        
        Returns:
            dict: Dictionary containing statistical measures for each subject
        """
        # Initialize subject marks dictionary
        subject_marks = {subject: [] for subject in ["Maths", "SST", "English", "Science"]}
        
        # Collecting marks for each student
        for student in self.students.values():
            for subject in subject_marks:
                mark = student.get_marks(subject)
                if mark is not None:
                    subject_marks[subject].append(mark)

        # Helper functions for statistics calculations
        def calc_average(marks):
            return format(sum(marks) / len(marks), '.4f') if marks else None
        
        def calc_mode_freq(marks):
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
            dict or None: Dictionary of student's grades if found, None otherwise
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


def print_with_animation(text, delay=0.03):
    """Print text with a typewriter animation effect."""
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def loading_animation(duration=1):
    """Display a simple loading animation."""
    for _ in range(int(duration * 10)):
        for char in '.....':
            print(f'\rLoading{char * 3}', end='', flush=True)
            time.sleep(0.1)
    print('\r' + ' ' * 20 + '\r', end='')

def print_menu():
    """Display the main menu options."""
    # Clear screen (using simple newlines instead of ANSI codes)
    print('\n' * 50)
    
    # Print header
    print('=' * 50)
    print('GRADEBOOK MANAGEMENT SYSTEM'.center(50))
    print('=' * 50)
    print()
    
    # Menu options without any color codes
    print('1 - Add student')
    print('2 - Delete student')
    print('3 - View statistics about grades')
    print('4 - View student grades')
    print('5 - Edit or Enter student grades')
    print('6 - Print Gradebook')
    print('m - Print menu')
    print('c - Clear Screen')
    print('q - Quit system')
    
    print('\n' + '=' * 50 + '\n')

def main():
    """Main function to run the gradebook application."""
    gradebook = Gradebook()
    
    print_with_animation("Starting Gradebook System...")
    loading_animation()
    
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()
        
        if choice == '1':
            print("\n=== Adding New Student ===")
            admin_no = input("Enter Admin Number: ").strip()
            name = input("Enter Student Name: ").strip()
            student = Student(admin_no, name)
            loading_animation(0.5)
            if gradebook.add_student(student):
                print(f"[SUCCESS] Student {name} added successfully.")
            else:
                print(f"[ERROR] Student with Admin Number {admin_no} already exists.")

        elif choice == '2':
            print("\n=== Deleting Student ===")
            admin_no = input("Enter Admin Number to delete: ").strip()
            loading_animation(0.5)
            if gradebook.delete_student(admin_no):
                print(f"[SUCCESS] Student with Admin Number {admin_no} deleted!")
            else:
                print("[ERROR] Student not found!")

        elif choice == '3':
            stats = gradebook.view_statistics()
            for stat, value in stats.items():
                print("-"*50)
                print(f"{stat}: {value}")
                print("-"*50)

        elif choice == '4':
            admin_no = input("Enter Admin Number to view grades: ").strip()
            grades = gradebook.view_student_grades(admin_no)
            if grades is not None:
                for key, value in grades.items():
                    print(f"{key}: {value}")
            else:
                print("Student not found.")

        elif choice == '5':
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
            data = gradebook_details = gradebook.print_gradebook()
            for key, value in data.items():
                print(f"{key}: {value}")
                

        elif choice == 'm':
            print_menu()

        elif choice == 'c':
            print('\n' * 50)  # Simple screen clear with newlines

        elif choice == 'q':
            print("\nSaving data...")
            gradebook.save_data()
            loading_animation(1)
            print("[GOODBYE] Thank you for using Gradebook System!")
            break
        else:
            print("[ERROR] Invalid choice. Please try again.")
        
        input("\nPress Enter to continue...")


if __name__ == "__main__":
    main()
