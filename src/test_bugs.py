def test_division_by_zero():
    """Function with potential division by zero bug"""
    def divide(a, b):
        return a / b  # Bug: no check for b == 0
    
    # This would cause an error: divide(10, 0)

def test_null_pointer():
    """Function with potential null pointer bug"""
    def get_length(text):
        return len(text)  # Bug: no check if text is None
    
    # This would cause an error: get_length(None)

def test_index_out_of_bounds():
    """Function with potential index out of bounds bug"""
    def get_item(lst, index):
        return lst[index]  # Bug: no bounds checking
    
    # This would cause an error: get_item([1, 2, 3], 10)

def test_insecure_input_handling():
    """Function with potential security vulnerability"""
    import subprocess
    
    def run_command(user_input):
        # Security bug: command injection vulnerability
        subprocess.run(user_input, shell=True)  # Dangerous!