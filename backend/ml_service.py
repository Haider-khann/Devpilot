import os
import re
import logging
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

logger = logging.getLogger(__name__)

class CodeMLService:
    def __init__(self, model_path='ml_models'):
        self.model_path = model_path
        os.makedirs(model_path, exist_ok=True)
        self.classifier = None
    
    def extract_features(self, code):
        return [
            len(code),
            len(code.splitlines()),
            # Python indicators
            len(re.findall(r'\bdef\b', code)),
            len(re.findall(r'\bimport\s+\w+', code)),
            len(re.findall(r'\bprint\s*\(', code)),
            len(re.findall(r'\bself\b', code)),
            code.count(':'),
            len(re.findall(r'#.*', code)),
            # JavaScript indicators
            len(re.findall(r'\bfunction\b', code)),
            len(re.findall(r'\bconst\b|\blet\b|\bvar\b', code)),
            len(re.findall(r'console\.log', code)),
            len(re.findall(r'=>', code)),
            code.count(';'),
            len(re.findall(r'[{}]', code)),
            # HTML indicators
            len(re.findall(r'<[a-z]+[^>]*>', code)),
            len(re.findall(r'</[a-z]+>', code)),
            len(re.findall(r'<!DOCTYPE', code, re.IGNORECASE)),
            len(re.findall(r'<html|<head|<body|<div|<p|<span', code)),
            # CSS indicators
            len(re.findall(r'[a-z-]+\s*:\s*[^;]+;', code)),
            len(re.findall(r'#[a-fA-F0-9]{3,6}', code)),
            len(re.findall(r'\.[a-z-]+\s*{', code)),
            len(re.findall(r'@media|@import', code)),
            # Markdown indicators
            len(re.findall(r'^#{1,6}\s', code, re.MULTILINE)),
            len(re.findall(r'\*\*.*\*\*', code)),
            len(re.findall(r'\[.*\]\(.*\)', code)),
            len(re.findall(r'^[-*]\s', code, re.MULTILINE)),
        ]
    
    def train_language_classifier(self, code_samples, languages):
        X = np.array([self.extract_features(c) for c in code_samples])
        y = np.array(languages)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        self.classifier = RandomForestClassifier(n_estimators=100, random_state=42)
        self.classifier.fit(X_train, y_train)
        
        y_pred = self.classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        joblib.dump(self.classifier, os.path.join(self.model_path, 'language_classifier.pkl'))
        
        return {
            'accuracy': round(accuracy * 100, 2),
            'training_samples': len(X_train),
            'test_samples': len(X_test)
        }
    
    def predict_language(self, code):
        if not self.classifier:
            model_file = os.path.join(self.model_path, 'language_classifier.pkl')
            if os.path.exists(model_file):
                self.classifier = joblib.load(model_file)
            else:
                return {'error': 'Model not trained yet'}
        
        vector = np.array(self.extract_features(code)).reshape(1, -1)
        prediction = self.classifier.predict(vector)[0]
        probabilities = self.classifier.predict_proba(vector)[0]
        confidence = round(max(probabilities) * 100, 2)
        
        return {'predicted_language': prediction, 'confidence': confidence}
    
    def get_sample_training_data(self):
        python_codes = [
            "def hello():\n    print('Hello')\n\nclass MyClass:\n    def method(self):\n        return 1",
            "import os\nimport sys\n\ndef main():\n    for i in range(10):\n        print(i)",
            "class BankAccount:\n    def __init__(self, balance):\n        self.balance = balance",
            "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)",
            "import json\nimport requests\n\ndef fetch(url):\n    r = requests.get(url)\n    return json.loads(r.text)",
            "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0]",
            "class Node:\n    def __init__(self, value):\n        self.value = value\n        self.left = None",
            "def deco(func):\n    def wrap(*args):\n        print('before')\n        return func(*args)\n    return wrap",
        ]
        
        js_codes = [
            "function hello() {\n    console.log('Hello');\n}\n\nclass MyClass {\n    method() { return 1; }\n}",
            "const express = require('express');\nconst app = express();\napp.get('/', (req, res) => res.send('Hello'));",
            "import React from 'react';\nfunction App() {\n    return <div>Hello</div>;\n}\nexport default App;",
            "const numbers = [1,2,3,4,5];\nconst doubled = numbers.map(n => n * 2);\nconsole.log(doubled);",
            "async function fetchData() {\n    const r = await fetch('https://api.com');\n    return r.json();\n}",
            "function total(items) {\n    let sum = 0;\n    for (let i = 0; i < items.length; i++) { sum += items[i]; }\n    return sum;\n}",
            "const person = { name: 'John', age: 30, greet() { return 'Hello'; } };",
            "export default class Component {\n    constructor(props) { this.props = props; }\n}",
        ]
        
        html_codes = [
            "<!DOCTYPE html>\n<html>\n<head><title>Page</title></head>\n<body><h1>Hello</h1></body>\n</html>",
            "<div class='container'>\n    <p>Text</p>\n    <a href='#'>Link</a>\n</div>",
            "<form action='/submit' method='POST'>\n    <input type='text' name='user'>\n    <button>Submit</button>\n</form>",
            "<table>\n    <tr><th>Name</th></tr>\n    <tr><td>John</td></tr>\n</table>",
        ]
        
        code_samples = python_codes + js_codes + html_codes
        languages = ['python'] * len(python_codes) + ['javascript'] * len(js_codes) + ['html'] * len(html_codes)
        
        css_codes = [
            "body { font-family: Arial; margin: 0; padding: 0; background: #fff; }",
            ".container { max-width: 1200px; margin: 0 auto; padding: 20px; }",
            ".header { background: #333; color: white; padding: 15px; }",
            ".btn { padding: 10px 20px; border-radius: 5px; cursor: pointer; }",
            "@media (max-width: 768px) { .container { padding: 10px; } }",
            ".card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-2px); }",
        ]
        
        md_codes = [
            "# Project Title\n\n## Description\nThis is a project.\n\n## Installation\n```\nnpm install\n```",
            "## Features\n- Feature 1\n- Feature 2\n\n## Usage\nSee documentation.",
            "# Heading\n\nSome text with **bold** and *italic*.\n\n![Image](url)",
            "## Table\n| Column 1 | Column 2 |\n|----------|----------|\n| Data 1 | Data 2 |",
        ]
        
        code_samples = python_codes + js_codes + html_codes + css_codes + md_codes
        languages = (['python'] * len(python_codes) + 
                    ['javascript'] * len(js_codes) + 
                    ['html'] * len(html_codes) +
                    ['css'] * len(css_codes) +
                    ['markdown'] * len(md_codes))
        
        return code_samples, languages