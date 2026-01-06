import os
import google.generativeai as genai
from typing import Dict, List
from dotenv import load_dotenv

load_dotenv()

class GeminiIntegration:
    """
    Handles integration with the Gemini API for code analysis.
    """

    def __init__(self):
        self.api_key = os.getenv('GEMINI_API_KEY')
        if not self.api_key:
            raise ValueError("GEMINI_API_KEY not found in environment variables")

        genai.configure(api_key=self.api_key)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
    
    def analyze_code_for_bugs(self, code: str, language: str = "python") -> Dict:
        """
        Analyze code for potential bugs using Gemini.
        """
        prompt = f"""
        You are an expert code reviewer. Analyze the following {language} code for potential bugs, 
        security vulnerabilities, performance issues, and code quality problems.
        
        Code:
        {code}
        
        Provide a detailed analysis in the following JSON format:
        {{
            "has_issues": true/false,
            "issues": [
                {{
                    "type": "bug_type",
                    "description": "detailed description of the issue",
                    "severity": "critical/high/medium/low",
                    "line_number": line_number,
                    "suggestion": "how to fix the issue",
                    "confidence": 0-100
                }}
            ],
            "code_quality_score": 0-100,
            "security_score": 0-100,
            "performance_score": 0-100
        }}
        
        Be specific about line numbers and provide actionable suggestions.
        """
        
        try:
            response = self.model.generate_content(prompt)
            # In a real implementation, we would parse the JSON response
            # For now, we'll return a mock response
            return {
                "has_issues": True,
                "issues": [
                    {
                        "type": "Logic Error",
                        "description": "Potential null pointer exception",
                        "severity": "high",
                        "line_number": 5,
                        "suggestion": "Add null check before accessing object",
                        "confidence": 85
                    }
                ],
                "code_quality_score": 70,
                "security_score": 65,
                "performance_score": 80
            }
        except Exception as e:
            error_msg = str(e)
            # Check if it's a quota exceeded error
            if "429" in error_msg or "quota" in error_msg.lower() or "rate limit" in error_msg.lower():
                return {
                    "error": f"API quota exceeded. Please check your billing details. {str(e)}",
                    "has_issues": False,
                    "issues": [],
                    "code_quality_score": 0,
                    "security_score": 0,
                    "performance_score": 0
                }
            else:
                return {
                    "error": f"Error calling Gemini API: {str(e)}",
                    "has_issues": False,
                    "issues": [],
                    "code_quality_score": 0,
                    "security_score": 0,
                    "performance_score": 0
                }
    
    def explain_fix(self, buggy_code: str, fixed_code: str) -> str:
        """
        Explain how the fixed code addresses the issues in the buggy code.
        """
        prompt = f"""
        Explain how the fixed code addresses the issues in the buggy code.
        
        Buggy Code:
        {buggy_code}
        
        Fixed Code:
        {fixed_code}
        
        Provide a clear explanation of what was wrong and how it was fixed.
        """
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error getting explanation: {str(e)}"