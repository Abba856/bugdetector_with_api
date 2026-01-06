import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

if not api_key or api_key == "your_gemini_api_key_here":
    print("API key not set or still using default value.")
    print("Please set your actual GEMINI_API_KEY in the .env file.")
else:
    print("Testing actual API functionality...")
    
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        
        # List available models
        models = genai.list_models()
        print("Available models:")
        for model in models:
            print(f"  - {model.name}")
            if 'generate_content' in model.supported_generation_methods:
                print(f"    Supports generate_content: Yes")
        
        # Try to find a suitable model
        suitable_model = None
        for model in models:
            if 'generate_content' in model.supported_generation_methods:
                if 'gemini' in model.name.lower():
                    suitable_model = model.name.split('/')[-1]  # Get just the model name part
                    break
        
        if suitable_model:
            print(f"\nUsing model: {suitable_model}")
            model = genai.GenerativeModel(suitable_model)
            
            # Test with a simple prompt
            test_prompt = "Hello, are you working?"
            response = model.generate_content(test_prompt)
            
            if response.text:
                print("✓ API is working correctly!")
                print(f"✓ Response received: {response.text[:100]}...")
            else:
                print("✗ API returned empty response")
        else:
            print("\nNo suitable model found that supports generate_content")
            
    except Exception as e:
        print(f"✗ Error during API test: {e}")