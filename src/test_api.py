import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the API key
api_key = os.getenv('GEMINI_API_KEY')

if not api_key or api_key == "your_gemini_api_key_here":
    print("API key not set or still using default value.")
    print("Please set your actual GEMINI_API_KEY in the .env file.")
    print("You can get an API key from: https://makersuite.google.com/app/apikey")
else:
    print("API key is set.")
    
    # Try to initialize the API
    try:
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        print("✓ Successfully configured the Google Generative AI client")
        
        # List available models as a test
        models = genai.list_models()
        print(f"✓ Successfully connected to API. Found {len(list(models))} models")
        
        # Get the generative model as another test
        model = genai.GenerativeModel('gemini-pro')
        print("✓ Successfully initialized the Gemini Pro model")
        
        print("\nAPI is working correctly!")
        
    except Exception as e:
        print(f"✗ Error connecting to API: {e}")
        print("This could be due to:")
        print("1. Invalid API key")
        print("2. Network connectivity issues")
        print("3. API not enabled in your Google Cloud project")