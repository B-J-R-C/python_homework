#q2
import csv
import traceback
import os
import custom_module
from datetime import datetime

def read_employees():
    # Declare empty dict and list
    result_dict = {}
    rows_list = []

    try:
        # Open the file using a relative path (up one level, then into csv folder)
        with open('../csv/employees.csv', 'r') as file:
            reader = csv.reader(file)
            
            # We use a flag to track if we are on the header row or data rows
            is_header = True
            
            for row in reader:
                if is_header:
                    # Store the first row (headers) in the dict
                    result_dict["fields"] = row
                    is_header = False
                else:
                    # Add all other rows to the list
                    rows_list.append(row)
            
            # Add the list of rows to the dict
            result_dict["rows"] = rows_list
            
            return result_dict

    except Exception as e:
        # Exception handling logic from Task 1
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

# Global variable assignment (Required for the test to pass)
employees = read_employees()

# Print to verify
print(employees)

#q3
def column_index(column_name):
    # Find the index of the column header in the employees dictionary
    return employees["fields"].index(column_name)

# Call the function and store the result in a global variable
employee_id_column = column_index("employee_id")

# Optional: Print it to see the result
print(f"Employee ID Column Index: {employee_id_column}")

#q4
def first_name(row_number):
    # Get the index for the "first_name" column
    col_idx = column_index("first_name")
    
    # Retrieve the specific row from the list of rows
    row = employees["rows"][row_number]
    
    # Return the value at that column index
    return row[col_idx]

#q5
def employee_find(employee_id):
    # Inner function to check for a match
    def employee_match(row):
        # We cast the CSV string data to an int for comparison
        return int(row[employee_id_column]) == employee_id

    # Use filter() to apply the match function to all rows
    matches = list(filter(employee_match, employees["rows"]))
    
    return matches
#q6
def employee_find_2(employee_id):
   # Filter using a lambda function for concise logic
   matches = list(filter(lambda row : int(row[employee_id_column]) == employee_id , employees["rows"]))
   return matches

#q7

def sort_by_last_name():
    # 1. Get the index of the column we want to sort by
    last_name_idx = column_index("last_name")
    
    # 2. Sort the rows list in-place using a lambda
    # The lambda tells sort() to look at the 'last_name_idx' of every row
    employees["rows"].sort(key=lambda row: row[last_name_idx])
    
    # 3. Return the sorted list
    return employees["rows"]

# Call the function to perform the sort (as requested by instructions)
sort_by_last_name()

# Print the entire dictionary to see that the rows are now alphabetical by last name
print(employees)

#q8

def employee_dict(row):
    emp_data = {}
    
    # zip() pairs the header with the value automatically
    for field, value in zip(employees["fields"], row):
        if field != "employee_id":
            emp_data[field] = value
            
    return emp_data

#q9
def all_employees_dict():
    # Create an empty dictionary to store the results
    all_emps = {}
    
    # Loop through every row in our global employees list
    for row in employees["rows"]:
        # Get the ID to use as the key (using the global index from Task 3)
        emp_id = row[employee_id_column]
        
        # Get the data dictionary (using the function from Task 8)
        emp_data = employee_dict(row)
        
        # Map the ID to the data
        all_emps[emp_id] = emp_data
        
    return all_emps

# Call the function and print the result
print(all_employees_dict())

#q10
def get_this_value():
    # Retrieve environment variable "THISVALUE"
    return os.getenv("THISVALUE")

#q11
def set_that_secret(new_secret):
    # Call the function inside the other module
    custom_module.set_secret(new_secret)

# Call the function to change the secret
set_that_secret("Open Sesame")

# Print the variable from the other module to verify it changed
print(custom_module.secret)

#q12
def read_file(filename):
    """Helper function to read a CSV and return a dict with rows as tuples."""
    result_dict = {}
    rows_list = []
    
    try:
        # Use f-string to construct the path
        with open(f'../csv/{filename}', 'r') as file:
            reader = csv.reader(file)
            
            is_header = True
            for row in reader:
                if is_header:
                    result_dict["fields"] = row
                    is_header = False
                else:
                    # Convert the row list to a TUPLE before adding
                    rows_list.append(tuple(row))
            
            result_dict["rows"] = rows_list
            return result_dict

    except Exception as e:
        print(f"Error reading {filename}: {e}")
        return {}

def read_minutes():
    # Reuse the helper function for both files
    m1 = read_file("minutes1.csv")
    m2 = read_file("minutes2.csv")
    return m1, m2

# Call the function and unpack the two returned values into global variables
minutes1, minutes2 = read_minutes()

# Verify the output
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
    # 1. Convert the set to a list
    raw_list = list(minutes_set)
    
    # 2. Use map() and lambda to convert the date string to a datetime object
    # x[0] is the name, x[1] is the date string
    processed_iterator = map(lambda x: (x[0], datetime.strptime(x[1], "%B %d, %Y")), raw_list)
    
    # 3. Convert the map result back to a list and return it
    return list(processed_iterator)

# Call the function and store in global variable
minutes_list = create_minutes_list()

# Print to verify (you will see datetime objects like datetime.datetime(2021, 3, 15...))
print(minutes_list)

#q15
def write_sorted_list():
    # 1. Sort the list by the date (the second element in the tuple)
    # Since they are datetime objects, Python knows how to sort them correctly
    minutes_list.sort(key=lambda x: x[1])
    
    # 2. Convert datetime objects back to strings using map
    # We create a new list where index 1 is formatted back to "Month Day, Year"
    formatted_list = list(map(lambda x: (x[0], datetime.strftime(x[1], "%B %d, %Y")), minutes_list))
    
    # 3. Write to the new CSV file
    # We use 'w' mode to write a new file
    with open('minutes.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        
        # Write the header row (using fields from minutes1)
        writer.writerow(minutes1["fields"])
        
        # Write all the data rows
        writer.writerows(formatted_list)
        
    return formatted_list

# Call the function to finish the assignment
sorted_minutes = write_sorted_list()

# Print "Done" to let you know it finished
print("All tasks complete! 'minutes.csv' has been created.")

