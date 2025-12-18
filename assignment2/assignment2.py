#q2
import csv
import traceback
import os
import custom_module
from datetime import datetime

def read_employees():
    # Declare empty
    result_dict = {}
    rows_list = []

    try:
        # Open relative path 
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            
            # flag to track
            is_header = True
            
            for row in reader:
                if is_header:
                    # Store first row 
                    result_dict["fields"] = row
                    is_header = False
                else:
                    # Add other row s
                    rows_list.append(row)
            
            
            result_dict["rows"] = rows_list
            
            return result_dict

    except Exception as e:
        # from Task 1
        trace_back = traceback.extract_tb(e.__traceback__)
        stack_trace = list()
        for trace in trace_back:
            stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
        
        print(f"Exception type: {type(e).__name__}")
        message = str(e)
        if message:
            print(f"Exception message: {message}")
        print(f"Stack trace: {stack_trace}")
        exit()

# need for test pass)
employees = read_employees()

# Print to check
print(employees)

#q3
def column_index(column_name):
    # Find index 
    return employees["fields"].index(column_name)

# Call 
employee_id_column = column_index("employee_id")

# Optional: Print to see if bad
print(f"Employee ID Column Index: {employee_id_column}")

#q4
def first_name(row_number):
    # Get index for the "first_name"
    col_idx = column_index("first_name")
    
    # row we want
    row = employees["rows"][row_number]
    
    
    return row[col_idx]

#q5
def employee_find(employee_id):
    # check for a match
    def employee_match(row):
        
        return int(row[employee_id_column]) == employee_id

    
    matches = list(filter(employee_match, employees["rows"]))
    
    return matches
#q6
def employee_find_2(employee_id):
   #  lambda filter function 
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches

#q7

def sort_by_last_name():
    
    last_name_idx = column_index("last_name")
    
    
    employees["rows"].sort(key=lambda row: row[last_name_idx])
    
    # 3. Retur sorted list
    return employees["rows"]

# Call
sort_by_last_name()

# Print all
print(employees)

#q8

def employee_dict(row):
    emp_data = {}
    
    
    for field, value in zip(employees["fields"], row):
        if field != "employee_id":
            emp_data[field] = value
            
    return emp_data

#q9
def all_employees_dict():
    # Create  dictionary 
    all_emps = {}
    
    # Loop 
    for row in employees["rows"]:
        
        emp_id = row[employee_id_column]
        
        
        emp_data = employee_dict(row)
        
        
        all_emps[emp_id] = emp_data
        
    return all_emps

# print
print(all_employees_dict())

#q10
def get_this_value():
    # Retrieve environment variable "THISVALUE"
    return os.getenv("THISVALUE")

#q11
def set_that_secret(new_secret):
    # Call 
    custom_module.set_secret(new_secret)

# Call the function to change the secret
set_that_secret("Open Sesame")

# Print 
print(custom_module.secret)

#q12
def read_file(filename):
    """Helper function to read a CSV and return a dict with rows as tuples."""
    result_dict = {}
    rows_list = []
    
    try:
        # Use f-string
        with open(f'../csv/{filename}', 'r') as file:
            reader = csv.reader(file)
            
            is_header = True
            for row in reader:
                if is_header:
                    result_dict["fields"] = row
                    is_header = False
                else:
                    # Convert  to a TUPLE before adding before
                    rows_list.append(tuple(row))
            
            result_dict["rows"] = rows_list
            return result_dict

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}

def read_minutes():
    
    m1 = read_file("minutes1.csv")
    m2 = read_file("minutes2.csv")
    return m1, m2


minutes1, minutes2 = read_minutes()

# Verify
print("Minutes 1:", minutes1)
print("Minutes 2:", minutes2)

#q13
def create_minutes_set():
    # Convert the list of tuples from each dictionary into a set
    set1 = set(minutes1["rows"])
    set2 = set(minutes2["rows"])
    
    # Create a union of the two sets (combines them and removes duplicates)
    combined_set = set1.union(set2)
    
    return combined_set

# Call the function and store it in a global variable
minutes_set = create_minutes_set()

# Optional: Print to see the unique set of minutes
print(f"Unique minutes count: {len(minutes_set)}")

#q14
def create_minutes_list():
    # 1. set to list
    raw_list = list(minutes_set)
    
    # x[0] is the name, x[1] is the date string
    processed_iterator = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), raw_list)
    
    # 3. back to a list 
    return list(processed_iterator)

# Call 
minutes_list = create_minutes_list()

# Print 
print(minutes_list)

#q15
def write_sorted_list():
    
    minutes_list.sort(key=lambda x: x[1])
    
    
    formatted_list = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list))
    
    
    with open('minutes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        
        writer.writerow(minutes1["fields"])
        
        
        writer.writerows(formatted_list)
        
    return formatted_list

# Call to finish the assignment att last
sorted_minutes = write_sorted_list()

# Print "Done" 
print("All tasks complete! 'minutes.csv' has been created.")

