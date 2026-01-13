#Q1
import traceback

try:
    # Open the file for appending ('a') using the 'with' statement
    # This automatically handles closing the file when the block ends
    with open("diary.txt", "a") as file:
        
        # We need a way to track if it is the first loop or not
        is_first_line = True
        
        while True:
            # Determine which prompt to show
            if is_first_line:
                user_input = input("What happened today? ")
                is_first_line = False
            else:
                user_input = input("What else? ")
            
            # Write the input to the file with a newline
            file.write(user_input + "\n")
            
            # Check for the exit condition
            if user_input == "done for now":
                break # This exits the loop (and the 'with' block closes the file)

except Exception as e:
    # The error handling code required by your assignment
    trace_back = traceback.extract_tb(e.__traceback__)
    stack_trace = list()
    for trace in trace_back:
        stack_trace.append(f'File : {trace[0]} , Line : {trace[1]}, Func.Name : {trace[2]}, Message : {trace[3]}')
    
    print(f"Exception type: {type(e).__name__}")
    message = str(e)
    if message:
        print(f"Exception message: {message}")
    print(f"Stack trace: {stack_trace}")

    
