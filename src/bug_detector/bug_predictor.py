from typing import Dict, List
from .gemini_integration import GeminiIntegration
from .data_collector import DataCollector

class BugPredictor:
    """
    Main bug prediction system that combines data collection and Gemini analysis.
    """
    
    def __init__(self):
        self.gemini = GeminiIntegration()
        self.data_collector = DataCollector()
    
    def predict_bugs(self, code: str, language: str = "python") -> Dict:
        """
        Predict potential bugs in the given code.
        """
        return self.gemini.analyze_code_for_bugs(code, language)
    
    def suggest_fix(self, code: str, issue_description: str) -> str:
        """
        Suggest a fix for a specific issue in the code.
        """
        prompt = f"""
        The following code has an issue: {issue_description}
        
        Code:
        {code}
        
        Please suggest a fix for this issue.
        """
        
        try:
            import google.generativeai as genai
            genai.configure(api_key=self.gemini.api_key)
            model = genai.GenerativeModel('gemini-2.5-flash')
            response = model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error suggesting fix: {str(e)}"
    
    def batch_predict(self, code_list: List[str]) -> List[Dict]:
        """
        Predict bugs for a list of code snippets.
        """
        results = []
        for i, code in enumerate(code_list):
            result = self.predict_bugs(code)
            result['code_index'] = i
            results.append(result)
        return results