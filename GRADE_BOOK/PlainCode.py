
import json
import statistics


# Student Information
STUDENT_NAME = "WANGODA FRANCIS"
STUDENT_NUMBER = "2400711855"
REGISTRATION_NUMBER = "24/U/11855/PS"


# Student class
class Student:
    def __init__(self, admin_no, name):
        # Initialising the student details and setting default marks to be zero
        self.admin_no = admin_no
        self.name = name
        self.marks = {
            "Maths": 0,
            "SST": 0,
            "English": 0,
            "Science": 0,
        }
        
    # setting marks for a specific subject
    def set_marks(self, subject, marks):
        if subject in self.marks and 0 <= marks <= 100:
            self.marks[subject] = marks
            return True
        return False
    
    # getting the student marks
    def get_marks(self, subject):
        return self.marks.get(subject) if 0 <= self.marks.get(subject) <= 100 else None
    
    # Editing the marks of the student
    def edit_marks(self, subject, new_marks):
        return self.set_marks(subject, new_marks) if subject else None


# Grade book class
class Gradebook:
    def __init__(self, filename='previous_data.json'):
        self.filename = filename
        self.students = {}
        self.load_data()
    
    # Loading the existing data
    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                data = json.load(file)
                for admin_no, info in data.items():
                    student = Student(admin_no, info['name'])
                    student.marks = info["marks"]
                    self.students[admin_no] = student
        except FileNotFoundError:
            print("Error! the file not found")
    
    # Saving the data onto the file
    def save_data(self):
        data = {admin_no:{"name": student.name,"marks": student.marks} for admin_no, student in self.students.items()}
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)

    # Adding a student to the grade book
    def add_student(self, student):
        if student.admin_no not in self.students:
            self.students[student.admin_no] = student
            self.save_data()
            return True
        return False
    
    # Returning student data
    def get_student(self, admin_no):
        return self.students.get(admin_no) if self.students.get(admin_no) else None
    
    # deleting a student from the system (grade book)
    def delete_student(self, admin_no):
        if admin_no in self.students:
            del self.students[admin_no]
            self.save_data()
            return True
        return False
    
    # Viewing subject statistics
    def view_statistics(self):
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
    
    # View the grades of a particular student
    def view_student_grades(self, admin_no):
        student = self.get_student(admin_no)
        if student:
            student_grades = {
                'Maths': student.marks["Maths"],
                'English': student.marks["English"],
                'Science': student.marks["Science"],
                'SST': student.marks["SST"]
            }
            return student_grades
        else:
            print("Student does not exist in the system!")

    # these are the details of the gradebook
    def print_gradebook(self):
        gradebook_details = {
            'total_students': len(self.students),
            'student_details': {admin_no: student.name for admin_no, student in self.students.items()}
        }
        return gradebook_details

# This is a menu for the user interaction
def print_menu():
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


# this function will be used to run the gradebook
def main():
    gradebook = Gradebook()
    while True:
        print_menu()
        choice = input("Select an option: ").strip().lower()
        
        if choice == '1':
            admin_no = input("Enter Admin Number: ").strip()
            name = input("Enter Student Name: ").strip()
            student = Student(admin_no,name)
            if gradebook.add_student(student):
                print(f"Student {name} added successfully.")
            else:
                print(f"Student with Admin Number {admin_no} already exists.")
        
        elif choice == '2':
            admin_no = input("Enter Admin Number to delete: ").strip()
            if gradebook.delete_student(admin_no):
                print(f"Student with Admin Number {admin_no} deleted!")
            else:
                print("Student not found!")

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
            print("\033c", end="")  # Clear screen

        elif choice == 'q':
            gradebook.save_data()
            print("Exiting the system. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()
