# Bug Detection System - Main Implementation

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BugDetector:
    """
    AI-driven bug detection system that uses Gemini API to identify potential bugs in code.
    """

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        # Initialize Gemini API client
        import google.generativeai as genai
        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')

    def analyze_code(self, code_snippet):
        """
        Analyze a code snippet for potential bugs using Gemini AI.

        Args:
            code_snippet (str): The code to analyze

        Returns:
            dict: Analysis results containing potential bugs and suggestions
        """
        prompt = f"""
        Analyze the following code for potential bugs, security vulnerabilities, and code quality issues.
        Provide specific details about what might be wrong and suggest fixes.

        Code:
        {code_snippet}

        Please return your response in the following JSON format:
        {{
            "has_bugs": true/false,
            "bugs": [
                {{
                    "type": "bug_type",
                    "description": "description of the issue",
                    "severity": "high/medium/low",
                    "line_number": line_number,
                    "suggestion": "how to fix it"
                }}
            ],
            "overall_score": 0-100 (higher is better code quality)
        }}
        """

        try:
            response = self.model.generate_content(prompt)
            # In a real implementation, we would parse the JSON response
            # For now, we'll return a mock response structure
            return {
                "has_bugs": True,
                "bugs": [
                    {
                        "type": "Logic Error",
                        "description": "Potential null pointer exception",
                        "severity": "high",
                        "line_number": 10,
                        "suggestion": "Add null check before accessing object"
                    }
                ],
                "overall_score": 75
            }
        except Exception as e:
            return {
                "error": f"Error analyzing code: {str(e)}",
                "has_bugs": False,
                "bugs": [],
                "overall_score": 0
            }

    def predict_bugs_in_file(self, file_path):
        """
        Analyze an entire file for potential bugs.

        Args:
            file_path (str): Path to the file to analyze

        Returns:
            dict: Analysis results for the entire file
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                code = file.read()
            return self.analyze_code(code)
        except FileNotFoundError:
            return {"error": f"File not found: {file_path}"}
        except Exception as e:
            return {"error": f"Error reading file: {str(e)}"}

    def batch_analyze(self, code_snippets):
        """
        Analyze multiple code snippets at once.

        Args:
            code_snippets (list): List of code snippets to analyze

        Returns:
            list: Analysis results for each snippet
        """
        results = []
        for i, snippet in enumerate(code_snippets):
            result = self.analyze_code(snippet)
            result['snippet_index'] = i
            results.append(result)
        return results

# Example usage
if __name__ == "__main__":
    detector = BugDetector()

    # Example code with potential bugs
    sample_code = """
    def calculate_average(numbers):
        total = 0
        for num in numbers:
            total += num
        return total / len(numbers)  # Potential division by zero

    def process_user_data(user_input):
        data = user_input.strip()
        return data.split(',')  # Potential issue if input is not a string
    """

    result = detector.analyze_code(sample_code)
    print("Bug Detection Results:")
    print(f"Has bugs: {result['has_bugs']}")
    print(f"Overall score: {result['overall_score']}")
    for bug in result['bugs']:
        print(f"- {bug['type']}: {bug['description']} (Line {bug['line_number']})")