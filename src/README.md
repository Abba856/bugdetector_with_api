# AI-Driven Bug Detection System

This project implements an AI-driven bug detection system that enhances software code reliability by automating the process of identifying and predicting software bugs during development.

## Features

- AI-powered code analysis using Google's Gemini API (using gemini-2.5-flash model)
- Detection of various types of bugs (logic errors, security vulnerabilities, performance issues)
- Real-time bug prediction during code writing
- Web interface for easy code analysis
- Evaluation metrics (accuracy, precision, recall, F1 score)

> **Note**: This implementation uses the `google-generativeai` package which has been deprecated.
> Google recommends switching to the `google.genai` package for future updates and bug fixes.

## Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your environment:
   - Create a `.env` file with your Gemini API key:
   ```
   GEMINI_API_KEY=your_actual_gemini_api_key_here
   ```

## Usage

### Command Line
```bash
python main.py
```

### Web Interface
```bash
python app.py
```
Then visit `http://localhost:5000`

## Project Structure

```
bug_detector_system/
├── requirements.txt
├── .env
├── main.py
├── bug_detector/
│   ├── __init__.py
│   ├── data_collector.py
│   ├── gemini_integration.py
│   ├── bug_predictor.py
│   └── evaluation.py
├── app.py
└── test_bugs.py
```

## Components

- `BugDetector`: Main class for analyzing code snippets
- `DataCollector`: Collects and preprocesses datasets of buggy/corrected code
- `GeminiIntegration`: Handles API calls to Gemini for code analysis
- `BugPredictor`: Main prediction system combining data collection and analysis
- `EvaluationMetrics`: Calculates performance metrics (accuracy, precision, recall)
- `app.py`: Web interface for real-time bug detection

## Testing

The system includes test cases in `test_bugs.py` with various types of bugs to verify the detection capabilities.

## Evaluation Metrics

The system evaluates performance using:
- Accuracy: Overall correctness of predictions
- Precision: Proportion of predicted bugs that are actually bugs
- Recall: Proportion of actual bugs that were caught
- F1 Score: Harmonic mean of precision and recall