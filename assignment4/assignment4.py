import pandas as pd


# Part 1: Create a DataFrame
# 
data = {
    'Name': ['Alice', 'Bob', 'Charlie'],
    'Age': [25, 30, 35],
    'City': ['New York', 'Los Angeles', 'Chicago']
}

task1_data_frame = pd.DataFrame(data)

print("--- 1. Original DataFrame ---")
print(task1_data_frame)
print("\n")



# Part 2: Add  new column (Salary)
# 
task1_with_salary = task1_data_frame.copy()
task1_with_salary['Salary'] = [70000, 80000, 90000]

print("--- 2. DataFrame with Salary ---")
print(task1_with_salary)
print("\n")



# Part 3: Modify existing column (Increment Age)
# 
task1_older = task1_with_salary.copy()
task1_older['Age'] += 1

print("--- 3. Modified DataFrame (Older) ---")
print(task1_older)
print("\n")



# Part 4: Save DataFrame as a CSV file
# 
task1_older.to_csv('employees.csv', index=False)
print("Successfully saved 'employees.csv'.")

print("--- 4. Verifying CSV File Content ---")
with open('employees.csv', 'r') as file:
    print(file.read())

# Task 2 

# 1. Load CSV file from Task 1
task2_employees = pd.read_csv('employees.csv')

print("--- Task 2 Part 1: Employees from CSV ---")
print(task2_employees)
print("\n")

import json

# Create a dummy JSON file
json_data = [
    {"Name": "Eve", "Age": 28, "City": "Miami", "Salary": 60000},
    {"Name": "Frank", "Age": 40, "City": "Seattle", "Salary": 95000}
]

with open('additional_employees.json', 'w') as f:
    json.dump(json_data, f)

# 2. Load JSON into DataFrame
json_employees = pd.read_json('additional_employees.json')

print("--- Task 2 Part 2: Employees from JSON ---")
print(json_employees)
print("\n")

# 3. Combine DataFrames
more_employees = pd.concat([task2_employees, json_employees], ignore_index=True)

print("--- Task 2 Part 3: Combined DataFrame ---")
print(more_employees)
print("\n")

#Task 3


# Task 3 Part 1: Use the head() method
# 

first_three = more_employees.head(3)

print("--- Task 3 Part 1: First 3 Rows ---")
print(first_three)
print("\n")



# Task 3 Part 2: tail() method

last_two = more_employees.tail(2)

print("--- Task 3 Part 2: Last 2 Rows ---")
print(last_two)
print("\n")


# Task 3 Part 3: Get the shape of the DataFrame
# Shape returns tuple
employee_shape = more_employees.shape

print("--- Task 3 Part 3: DataFrame Shape ---")
print(employee_shape)
print("\n")



# Task 3 Part 4: Use info() method

print("--- Task 3 Part 4: DataFrame Info ---")
# .info() prints directly to  console
more_employees.info()
print("\n")


# Task 4

import pandas as pd
import numpy as np


# Task 4 Part 1: Load Dirty Data

dirty_data = pd.read_csv('dirty_data.csv')

print("--- Task 4 Part 1: Original Dirty Data ---")
print(dirty_data)
print("\n")


# Task 4 Part 2: Remove Duplicates
# Create a copy to clean
clean_data = dirty_data.copy()

# Remove duplicate rows
clean_data = clean_data.drop_duplicates()

print("--- Task 4 Part 2: Duplicates Removed ---")
print(clean_data)
print("\n")


# Task 4 Part 3: Convert Age to Numeric
# errors='coerce' turns non-numbers to NaN values
clean_data['Age'] = pd.to_numeric(clean_data['Age'], errors='coerce')

print("--- Task 4 Part 3: Age Converted (with NaNs) ---")
print(clean_data)
print("\n")


# Task 4 Part 4: Convert Salary to Numeric
# 'unknown', 'n/a'  coerced to NaN
clean_data['Salary'] = pd.to_numeric(clean_data['Salary'], errors='coerce')

print("--- Task 4 Part 4: Salary Converted (with NaNs) ---")
print(clean_data)
print("\n")


# Task 4 Part 5: Fill Missing Values (Imputation)
# Calculate mean age and& median salary
mean_age = clean_data['Age'].mean()
median_salary = clean_data['Salary'].median()

# Fill the missing values (NaNs) with:
clean_data['Age'] = clean_data['Age'].fillna(mean_age)
clean_data['Salary'] = clean_data['Salary'].fillna(median_salary)

print("--- Task 4 Part 5: Missing Values Filled ---")
print(clean_data)
print("\n")


# Task 4 Part 6: Convert Hire Date
clean_data['Hire Date'] = pd.to_datetime(clean_data['Hire Date'])

print("--- Task 4 Part 6: Dates Standardized ---")
print(clean_data)
print("\n")


# Task 4 Part 7: String Manipulation (Strip & Uppercase)
# Standardise Name and Department
clean_data['Name'] = clean_data['Name'].str.strip().str.upper()
clean_data['Department'] = clean_data['Department'].str.strip().str.upper()

print("--- Task 4 Part 7: Strings Cleaned (Final) ---")
print(clean_data)
print("\n")