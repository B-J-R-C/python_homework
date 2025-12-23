import logging
import functools

#  Logging Setup
logger = logging.getLogger(__name__ + "_parameter_log")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler("./decorator.log", "a")
logger.addHandler(file_handler)

def logger_decorator(func):
    
    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        result = func(*args, **kwargs)
        
        
        pos_params = list(args) if args else "none"
        
        
        key_params = kwargs if kwargs else "none"
        
        # log message
        log_message = (
            f"\nfunction: {func.__name__}\n"
            f"positional parameters: {pos_params}\n"
            f"keyword parameters: {key_params}\n"
            f"return: {result}"
        )
        
        
        logger.log(logging.INFO, log_message)
        
        return result
    return wrapper

# Function Defs

# 1. No param= nothing
@logger_decorator
def say_hello():
    print(">> Inside say_hello: Hello, World!")

# 2. Variable = True
@logger_decorator
def process_positional(*args):
    return True


@logger_decorator
def process_keywords(**kwargs):
    # Return function object
    return logger_decorator

# --- Mainline Code ---
if __name__ == "__main__":
    print("Running Task 1 tests...\n")

    # Test  1
    print("1. Calling say_hello()...")
    say_hello()
    print("-" * 20)

    # Test 2
    print("2. Calling process_positional(10, 20, 'apple')...")
    ret_val_2 = process_positional(10, 20, "apple")
    print(f"   Return value: {ret_val_2}")
    print("-" * 20)

    # Test 3
    print("3. Calling process_keywords(status='active', id=404)...")
    ret_val_3 = process_keywords(status="active", id=404)
    print(f"   Return value: {ret_val_3}")
    print("-" * 20)

    print("Done. Please check ./decorator.log for results.")

    #Q2
    import functools

def type_converter(type_of_output):
    
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Execute 1st function
            x = func(*args, **kwargs)
            # Convert a& return result
            return type_of_output(x)
        return wrapper
    return decorator

# 1. Function returning 5 (int)
@type_converter(str)
def return_int():
    return 5

# 2. Function returning "not a number"
@type_converter(int)
def return_string():
    return "not a number"


if __name__ == "__main__":
    
    # Test 1
    y = return_int()
    print(f"Result: {y}") 
    print(type(y).__name__) 

    # Test 2
    try:
       y = return_string()
       print("shouldn't get here!")
    except ValueError:
       print("can't convert that string to an integer!") # what should happen

       #q3
import csv
import os

# path to CSV file
file_path = '../csv/employees.csv'

try:
    with open(file_path, 'r', newline='') as csvfile:
        
        reader = csv.reader(csvfile)
        data = list(reader)

    # --- Task 1:list of full names ---
    
    full_names = [f"{row[1]} {row[2]}" for row in data[1:]]
    
    print("--- List of Full Names ---")
    print(full_names)

    # --- Task 2: Filter names containing 'e' ---
    
    names_with_e = [name for name in full_names if "e" in name]

    print("\n--- Names containing 'e' ---")
    print(names_with_e)

except FileNotFoundError:
    print(f"Error: Could not find file at {file_path}")
    print("Please ensure the folder '../csv' exists and contains 'employees.csv'.")
except IndexError:
    print("Error: The CSV columns didn't match the expected indices.")
    print("Check that your CSV has at least 3 columns (e.g., ID, First, Last).")

    #q4
