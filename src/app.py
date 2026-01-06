from flask import Flask, request, jsonify, render_template_string
from bug_detector.bug_predictor import BugPredictor

app = Flask(__name__)
predictor = BugPredictor()

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Bug Detector - Advanced Code Analysis</title>
    <link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Source+Code+Pro:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --primary-color: #4361ee;
            --secondary-color: #3f37c9;
            --success-color: #4cc9f0;
            --warning-color: #f72585;
            --danger-color: #e63946;
            --light-color: #f8f9fa;
            --dark-color: #212529;
            --gray-color: #6c757d;
            --border-radius: 12px;
            --box-shadow: 0 10px 20px rgba(0,0,0,0.1);
            --transition: all 0.3s ease;
        }

        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        body {
            font-family: 'Roboto', sans-serif;
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
            color: var(--dark-color);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }

        .container {
            max-width: 1200px;
            margin: 0 auto;
        }

        header {
            text-align: center;
            margin-bottom: 30px;
            padding: 20px;
        }

        h1 {
            font-size: 2.5rem;
            color: var(--secondary-color);
            margin-bottom: 10px;
            font-weight: 700;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        }

        .subtitle {
            font-size: 1.2rem;
            color: var(--gray-color);
            margin-bottom: 20px;
        }

        .card {
            background: white;
            border-radius: var(--border-radius);
            box-shadow: var(--box-shadow);
            padding: 30px;
            margin-bottom: 30px;
            transition: var(--transition);
        }

        .card:hover {
            box-shadow: 0 15px 30px rgba(0,0,0,0.15);
            transform: translateY(-5px);
        }

        .form-group {
            margin-bottom: 20px;
        }

        label {
            display: block;
            margin-bottom: 10px;
            font-weight: 500;
            color: var(--dark-color);
            font-size: 1.1rem;
        }

        textarea {
            width: 100%;
            height: 300px;
            padding: 15px;
            border: 2px solid #e9ecef;
            border-radius: var(--border-radius);
            font-family: 'Source Code Pro', monospace;
            font-size: 16px;
            resize: vertical;
            transition: var(--transition);
        }

        textarea:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(67, 97, 238, 0.2);
        }

        .btn {
            display: inline-block;
            padding: 14px 28px;
            background: linear-gradient(135deg, var(--primary-color) 0%, var(--secondary-color) 100%);
            color: white;
            border: none;
            border-radius: var(--border-radius);
            font-size: 1.1rem;
            font-weight: 500;
            cursor: pointer;
            transition: var(--transition);
            text-align: center;
            box-shadow: 0 4px 15px rgba(67, 97, 238, 0.3);
        }

        .btn:hover:not(:disabled) {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(67, 97, 238, 0.4);
        }

        .btn:disabled {
            background: #cccccc;
            cursor: not-allowed;
            transform: none;
            box-shadow: none;
        }

        .btn-analyzing {
            background: linear-gradient(135deg, #4cc9f0 0%, #4895ef 100%);
        }

        .result {
            margin-top: 30px;
            padding: 25px;
            border-radius: var(--border-radius);
            background: white;
            box-shadow: var(--box-shadow);
            display: none;
        }

        .result-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            padding-bottom: 15px;
            border-bottom: 2px solid #e9ecef;
        }

        .result-title {
            font-size: 1.5rem;
            color: var(--secondary-color);
            font-weight: 600;
        }

        .score-container {
            display: flex;
            gap: 15px;
            margin-top: 15px;
            flex-wrap: wrap;
        }

        .score-box {
            background: #f8f9fa;
            padding: 15px;
            border-radius: var(--border-radius);
            min-width: 150px;
            text-align: center;
            border: 1px solid #e9ecef;
        }

        .score-value {
            font-size: 2rem;
            font-weight: 700;
            margin-bottom: 5px;
        }

        .score-label {
            font-size: 0.9rem;
            color: var(--gray-color);
        }

        .issues-container {
            margin-top: 20px;
        }

        .issues-header {
            font-size: 1.3rem;
            color: var(--danger-color);
            margin-bottom: 15px;
            padding-bottom: 10px;
            border-bottom: 1px solid #e9ecef;
        }

        .issue-item {
            background: #fff5f5;
            border-left: 4px solid var(--danger-color);
            padding: 15px;
            margin-bottom: 15px;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
        }

        .issue-type {
            font-weight: 600;
            color: var(--danger-color);
            margin-bottom: 5px;
        }

        .issue-description {
            margin-bottom: 8px;
        }

        .issue-suggestion {
            font-style: italic;
            color: var(--gray-color);
        }

        .no-issues {
            background: #f0fff4;
            border-left: 4px solid #28a745;
            padding: 20px;
            text-align: center;
            border-radius: 0 var(--border-radius) var(--border-radius) 0;
        }

        .no-issues-text {
            color: #28a745;
            font-size: 1.1rem;
            font-weight: 500;
        }

        .processing {
            color: var(--primary-color);
            font-style: italic;
            font-size: 1.1rem;
            text-align: center;
            padding: 20px;
        }

        .error {
            color: var(--danger-color);
            background: #fff5f5;
            padding: 15px;
            border-radius: var(--border-radius);
            border-left: 4px solid var(--danger-color);
        }

        .features {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin-top: 40px;
        }

        .feature-card {
            background: white;
            padding: 25px;
            border-radius: var(--border-radius);
            text-align: center;
            box-shadow: 0 5px 15px rgba(0,0,0,0.05);
            transition: var(--transition);
        }

        .feature-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 10px 25px rgba(0,0,0,0.1);
        }

        .feature-icon {
            font-size: 2.5rem;
            color: var(--primary-color);
            margin-bottom: 15px;
        }

        .feature-title {
            font-size: 1.2rem;
            margin-bottom: 10px;
            color: var(--secondary-color);
        }

        footer {
            text-align: center;
            margin-top: 40px;
            padding: 20px;
            color: var(--gray-color);
            font-size: 0.9rem;
        }

        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }

            h1 {
                font-size: 2rem;
            }

            .card {
                padding: 20px;
            }

            textarea {
                height: 250px;
            }

            .score-container {
                flex-direction: column;
            }

            .score-box {
                min-width: auto;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <h1>🤖 AI-Powered Bug Detector</h1>
            <p class="subtitle">Advanced code analysis using artificial intelligence</p>
        </header>

        <main>
            <div class="card">
                <form id="bugForm">
                    <div class="form-group">
                        <label for="code">Enter your code to analyze:</label>
                        <textarea id="code" name="code" placeholder="// Paste your code here...

function example() {
    let x = 10 / 0; // Potential division by zero
    return x;
}"></textarea>
                    </div>
                    <button type="submit" class="btn" id="submitBtn">🔍 Detect Bugs</button>
                </form>
            </div>

            <div id="result" class="result">
                <div class="result-header">
                    <h3 class="result-title">Analysis Results</h3>
                </div>
                <div id="result-content"></div>
            </div>
        </main>

        <div class="features">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <h3 class="feature-title">Real-time Analysis</h3>
                <p>Get instant feedback on your code quality and potential bugs</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔍</div>
                <h3 class="feature-title">Deep Inspection</h3>
                <p>Advanced AI detects complex bugs and security vulnerabilities</p>
            </div>
            <div class="feature-card">
                <div class="feature-icon">📊</div>
                <h3 class="feature-title">Detailed Metrics</h3>
                <p>Comprehensive scoring for code quality, security, and performance</p>
            </div>
        </div>

        <footer>
            <p>AI Bug Detector System &copy; 2026 | Powered by Gemini AI</p>
        </footer>
    </div>

    <script>
        document.getElementById('bugForm').addEventListener('submit', function(e) {
            e.preventDefault();

            const code = document.getElementById('code').value;
            const submitBtn = document.getElementById('submitBtn');
            const resultDiv = document.getElementById('result');
            const resultContent = document.getElementById('result-content');

            if (!code.trim()) {
                alert('Please enter some code to analyze.');
                return;
            }

            // Show processing message and disable button
            resultContent.innerHTML = '<p class="processing">🔍 Analyzing your code... Please wait while our AI examines your code for potential bugs.</p>';
            resultDiv.style.display = 'block';
            submitBtn.disabled = true;
            submitBtn.textContent = '🔍 Analyzing...';
            submitBtn.classList.add('btn-analyzing');

            fetch('/analyze', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({code: code})
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    resultContent.innerHTML = '<div class="error">❌ Error: ' + data.error + '</div>';
                    return;
                }

                let html = '';

                // Create score boxes
                html += '<div class="score-container">';
                html += '<div class="score-box">';
                html += '<div class="score-value">' + (data.code_quality_score || 0) + '</div>';
                html += '<div class="score-label">Code Quality</div>';
                html += '</div>';

                html += '<div class="score-box">';
                html += '<div class="score-value">' + (data.security_score || 0) + '</div>';
                html += '<div class="score-label">Security</div>';
                html += '</div>';

                html += '<div class="score-box">';
                html += '<div class="score-value">' + (data.performance_score || 0) + '</div>';
                html += '<div class="score-label">Performance</div>';
                html += '</div>';

                html += '</div>';

                // Show issues if any
                if (data.issues && data.issues.length > 0) {
                    html += '<h4 class="issues-header">⚠️ Issues Found (' + data.issues.length + ')</h4>';
                    html += '<div class="issues-container">';

                    data.issues.forEach(issue => {
                        html += '<div class="issue-item">';
                        html += '<div class="issue-type">' + issue.type + ' (Line ' + (issue.line_number || 'N/A') + ')</div>';
                        html += '<div class="issue-description">' + issue.description + '</div>';
                        html += '<div class="issue-suggestion">💡 Suggestion: ' + issue.suggestion + '</div>';

                        // Add additional context from Serper if available
                        if (issue.additional_context) {
                            html += '<div class="issue-external-context" style="margin-top: 10px; padding: 10px; background: #e6f7ff; border-radius: 6px; border-left: 3px solid #1890ff;">';
                            html += '<strong>📚 Additional Info:</strong><br>';
                            html += '<a href="' + issue.additional_context.link + '" target="_blank" style="color: #1890ff; text-decoration: none;">';
                            html += issue.additional_context.title + '</a><br>';
                            html += '<small style="color: #666;">' + issue.additional_context.snippet + '</small>';
                            html += '</div>';
                        }

                        html += '</div>';
                    });

                    html += '</div>';
                } else {
                    html += '<div class="no-issues">';
                    html += '<p class="no-issues-text">🎉 No issues detected! Your code looks great.</p>';
                    html += '</div>';
                }

                resultContent.innerHTML = html;
            })
            .catch(error => {
                resultContent.innerHTML = '<div class="error">❌ Network error: ' + error + '</div>';
            })
            .finally(() => {
                // Re-enable button and update text
                submitBtn.disabled = false;
                submitBtn.textContent = '🔍 Detect Bugs';
                submitBtn.classList.remove('btn-analyzing');
            });
        });
    </script>
</body>
</html>
'''

@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)

@app.route('/analyze', methods=['POST'])
def analyze():
    data = request.json
    code = data.get('code', '')
    
    if not code:
        return jsonify({'error': 'No code provided'}), 400
    
    result = predictor.predict_bugs(code)
    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)