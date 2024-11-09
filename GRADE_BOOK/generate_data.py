import json
import random
import names  # you'll need to install this: pip install names

def generate_random_data(num_records=200):
    """Generate random student records with marks."""
    data = {}
    
    # Generate admin numbers from 2400711001 to 2400711200
    admin_start = 2400711001
    
    for i in range(num_records):
        admin_no = str(admin_start + i)
        student_name = names.get_full_name()
        
        # Generate random marks between 40 and 100 for each subject
        marks = {
            "Maths": random.randint(40, 100),
            "SST": random.randint(40, 100),
            "English": random.randint(40, 100),
            "Science": random.randint(40, 100)
        }
        
        # Create student record
        data[admin_no] = {
            "name": student_name,
            "marks": marks
        }
    
    # Save to JSON file
    with open('previous_data.json', 'w') as f:
        json.dump(data, f, indent=4)
    
    print(f"Successfully generated {num_records} random student records!")

if __name__ == "__main__":
    generate_random_data() 