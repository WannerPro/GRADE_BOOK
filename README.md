# Gradebook Management System

A command-line application for managing student grades and academic records, with support for statistical analysis and persistent data storage.

## Author
- Name: WANGODA FRANCIS
- Student Number: 2400711855
- Registration Number: 24/U/11855/PS

## Features

- Add and remove students with unique administrative numbers
- Record and edit grades for multiple subjects (Maths, SST, English, Science)
- View individual student grades and academic progress
- Generate comprehensive statistical analysis including:
  - Average scores per subject
  - Maximum and minimum grades
  - Mode and frequency analysis
- Save data persistently using JSON format
- Simple and intuitive command-line interface
- Input validation for grades (0-100 range)
- Clear error handling and user feedback

## Project Structure

GRADE_BOOK/

### Detailed Component Structure

#### 1. Student Class
- **Purpose**: Manages individual student data
- **Attributes**:
  - `admin_no`: Unique identifier
  - `name`: Student's full name
  - `marks`: Dictionary of subject marks
- **Methods**:
  - `__init__(admin_no, name)`: Initialize student
  - `set_marks(subject, marks)`: Set subject marks
  - `get_marks(subject)`: Retrieve marks
  - `edit_marks(subject, new_marks)`: Modify marks

#### 2. Gradebook Class
- **Purpose**: Manages entire gradebook system
- **Attributes**:
  - `filename`: JSON storage location
  - `students`: Dictionary of Student objects
- **Methods**:
  - `__init__(filename)`: Initialize gradebook
  - `load_data()`: Load from JSON
  - `save_data()`: Save to JSON
  - `add_student(student)`: Add new student
  - `get_student(admin_no)`: Retrieve student
  - `delete_student(admin_no)`: Remove student
  - `view_statistics()`: Calculate statistics
  - `view_student_grades(admin_no)`: View grades
  - `print_gradebook()`: System summary

#### 3. Data Storage Structure

The application uses JSON format for data persistence. The data is stored in `previous_data.json` with the following structure:

##### Data Structure Details:

1. **Root Level**
   - Key: Student's administrative number (string)
   - Value: Object containing student details

2. **Student Object**
   - `name`: Student's full name (string)
   - `marks`: Object containing subject marks

3. **Marks Object**
   - `Maths`: Mathematics score (integer: 0-100)
   - `SST`: Social Studies score (integer: 0-100)
   - `English`: English score (integer: 0-100)
   - `Science`: Science score (integer: 0-100)

##### Data Validation:
- Admin numbers must be unique
- Marks must be between 0 and 100
- All subject marks are required
- Names cannot be empty

##### File Operations:
1. **Reading Data**
   - Loads on program startup
   - Converts JSON to Student objects
   - Handles missing file errors

2. **Writing Data**
   - Saves after every modification
   - Converts Student objects to JSON
   - Maintains data persistence

3. **Data Security**
   - Backup creation recommended
   - File permissions should be set appropriately
   - Error handling for file operations

##### Sample Data Generation:
The `generate_data.py` script creates sample records following this structure:
- Creates 200 random student records
- Generates realistic names
- Assigns random marks between 40-100
- Maintains data structure integrity
