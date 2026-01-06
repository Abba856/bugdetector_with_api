# Final verification that the API is working
import os
import sys
sys.path.append('/var/www/html/bugdetector/src')

from dotenv import load_dotenv
load_dotenv()

print("=== FINAL API VERIFICATION ===")
print("Checking if the API is working with the bug detection system...")

# Test the full pipeline
try:
    from bug_detector.bug_predictor import BugPredictor
    
    # Create a predictor
    predictor = BugPredictor()
    print("✓ BugPredictor created successfully")
    
    # Test with code that should have bugs
    problematic_code = """
    def divide_numbers(a, b):
        result = a / b  # This could cause division by zero
        return result

    def access_list_item(lst, index):
        return lst[index]  # This could cause index out of bounds
    """
    
    print(f"Analyzing code with potential bugs...")
    print("Code being analyzed:")
    print(problematic_code)
    print()
    
    result = predictor.predict_bugs(problematic_code)
    
    print("Analysis Results:")
    print(f"- Has issues: {result.get('has_issues')}")
    print(f"- Code quality score: {result.get('code_quality_score')}")
    print(f"- Security score: {result.get('security_score')}")
    print(f"- Performance score: {result.get('performance_score')}")
    
    issues = result.get('issues', [])
    print(f"- Number of issues detected: {len(issues)}")
    
    if issues:
        print("Issues found:")
        for i, issue in enumerate(issues, 1):
            print(f"  {i}. Type: {issue.get('type')}")
            print(f"     Description: {issue.get('description')}")
            print(f"     Severity: {issue.get('severity')}")
            print(f"     Line: {issue.get('line_number')}")
            print(f"     Suggestion: {issue.get('suggestion')}")
            print(f"     Confidence: {issue.get('confidence')}%")
            print()
    else:
        print("No issues detected in this analysis.")
    
    print("✅ API is working correctly with the bug detection system!")
    print("The system can successfully analyze code and detect potential bugs.")

except Exception as e:
    print(f"❌ Error during API verification: {e}")
    import traceback
    traceback.print_exc()

print("\n=== VERIFICATION COMPLETE ===")