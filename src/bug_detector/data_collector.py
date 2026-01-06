import os
import json
import requests
from typing import List, Dict, Tuple

class DataCollector:
    """
    Collects and preprocesses datasets of buggy and corrected code samples.
    """
    
    def __init__(self):
        self.datasets = []
    
    def collect_from_github(self, repo_url: str, language: str = "python") -> List[Dict]:
        """
        Collect code samples from GitHub repositories.
        Note: This is a simplified implementation.
        """
        # In a real implementation, you would use the GitHub API to collect code samples
        # For now, we'll return a mock dataset
        return [
            {
                "buggy_code": "def divide(a, b):\n    return a / b  # Potential division by zero",
                "fixed_code": "def divide(a, b):\n    if b == 0:\n        raise ValueError('Cannot divide by zero')\n    return a / b",
                "language": language,
                "bug_type": "division_by_zero"
            },
            {
                "buggy_code": "def get_item(lst, index):\n    return lst[index]  # Potential index out of bounds",
                "fixed_code": "def get_item(lst, index):\n    if 0 <= index < len(lst):\n        return lst[index]\n    else:\n        return None",
                "language": language,
                "bug_type": "index_out_of_bounds"
            }
        ]
    
    def load_local_dataset(self, file_path: str) -> List[Dict]:
        """
        Load a dataset from a local JSON file.
        """
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Dataset file not found: {file_path}")
            return []
        except json.JSONDecodeError:
            print(f"Invalid JSON in dataset file: {file_path}")
            return []
    
    def preprocess_code(self, code: str) -> str:
        """
        Preprocess code for analysis.
        """
        # Remove extra whitespace and normalize the code
        lines = [line.strip() for line in code.split('\n') if line.strip()]
        return '\n'.join(lines)
    
    def get_training_data(self) -> Tuple[List[str], List[str]]:
        """
        Get preprocessed training data (buggy code, fixed code).
        """
        buggy_codes = []
        fixed_codes = []
        
        for item in self.datasets:
            buggy_codes.append(self.preprocess_code(item['buggy_code']))
            fixed_codes.append(self.preprocess_code(item['fixed_code']))
        
        return buggy_codes, fixed_codes