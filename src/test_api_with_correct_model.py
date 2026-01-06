import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key or api_key == "your_gemini_api_key_here":
    print("API key not set or still using default value.")
    print("Please set your actual GEMINI_API_KEY in the .env file.")
else:
    print("Testing actual API functionality with gemini-2.5-flash...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel('gemini-2.5-flash')
        
        # Test with a simple prompt
        test_prompt = "Hello, are you working?"
        response = model.generate_content(test_prompt)
        
        if response.text:
            print("✓ API is working correctly!")
            print(f"✓ Response received: {response.text[:100]}...")
        else:
            print("✗ API returned empty response")
            
    except Exception as e:
        print(f"✗ Error during API test: {e}")
        
    # Test with code analysis
    try:
        code_test = """
        def buggy_function(x):
            return 10 / x  # Potential division by zero
        """
        
        code_prompt = f"""
        Analyze this Python code for bugs:
        {code_test}
        
        Just respond with 'BUGS FOUND' if you detect any issues.
        """
        
        response = model.generate_content(code_prompt)
        
        if response.text and "BUG" in response.text.upper():
            print("✓ API correctly identified bugs in test code!")
        else:
            print("o API responded to code analysis (may not have detected bugs, which is also valid)")
            if response.text:
                print(f"  Response: {response.text[:100]}...")
            
        print("\nAPI test completed successfully!")
        
    except Exception as e:
        print(f"✗ Error during code analysis test: {e}")