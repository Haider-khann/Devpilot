import os
import re
import logging
import joblib
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

logger = logging.getLogger(__name__)

class CodeMLService:
    def __init__(self, model_path='ml_models'):
        self.model_path = model_path
        os.makedirs(model_path, exist_ok=True)
        self.classifier = None
        self.quality_classifier = None
    
    def extract_features(self, code):
        return [
            len(code),
            len(code.splitlines()),
            len(re.findall(r'\bdef\b', code)),
            len(re.findall(r'\bimport\s+\w+', code)),
            len(re.findall(r'\bprint\s*\(', code)),
            len(re.findall(r'\bself\b', code)),
            code.count(':'),
            len(re.findall(r'#.*', code)),
            len(re.findall(r'\bfunction\b', code)),
            len(re.findall(r'\bconst\b|\blet\b|\bvar\b', code)),
            len(re.findall(r'console\.log', code)),
            len(re.findall(r'=>', code)),
            code.count(';'),
            len(re.findall(r'[{}]', code)),
            len(re.findall(r'<[a-z]+[^>]*>', code)),
            len(re.findall(r'</[a-z]+>', code)),
            len(re.findall(r'<!DOCTYPE', code, re.IGNORECASE)),
            len(re.findall(r'<html|<head|<body|<div|<p|<span', code)),
            len(re.findall(r'[a-z-]+\s*:\s*[^;]+;', code)),
            len(re.findall(r'#[a-fA-F0-9]{3,6}', code)),
            len(re.findall(r'\.[a-z-]+\s*\{', code)),
            len(re.findall(r'@media|@import', code)),
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
        return {'accuracy': round(accuracy * 100, 2), 'training_samples': len(X_train), 'test_samples': len(X_test)}
    
    def predict_language(self, code):
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
    
    def train_quality_model(self):
        good = [
            "def calculate_total(items):\n    total = 0\n    for item in items:\n        total += item.price\n    return total",
            "class User:\n    def __init__(self, name):\n        self.name = name\n\n    def greet(self):\n        return f'Hello, {self.name}'",
            "def fetch_data(url):\n    try:\n        response = requests.get(url)\n        return response.json()\n    except Exception as e:\n        print(f'Error: {e}')\n        return None",
            "function calculateSum(numbers) {\n    return numbers.reduce((sum, num) => sum + num, 0);\n}",
            "const validateEmail = (email) => {\n    const regex = /^[^\\s@]+@[^\\s@]+\\.[^\\s@]+$/;\n    return regex.test(email);\n};",
            "def calculate_average(numbers):\n    if not numbers:\n        return 0\n    return sum(numbers) / len(numbers)",
            "def is_prime(n):\n    if n < 2:\n        return False\n    for i in range(2, int(n**0.5) + 1):\n        if n % i == 0:\n            return False\n    return True",
            "class BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n\n    def deposit(self, amount):\n        if amount > 0:\n            self.balance += amount\n            return True\n        return False",
            "function sortByDate(items) {\n    return items.sort((a, b) => new Date(b.date) - new Date(a.date));\n}",
            "const formatPrice = (price) => {\n    return `$${price.toFixed(2)}`;\n};",
        ]
        bad = [
            "def f(x):\n    return x+1",
            "x=10\ny=20\nz=x+y\nprint(z)",
            "def do_stuff():\n    pass",
            "function x() { return 1; }",
            "const a = 5; const b = 10; console.log(a + b);",
            "def q():\n    global x\n    x = x + 1",
            "a=1\nb=2\nc=a+b",
            "def x(a,b):\n    return a*b",
            "function y(){return 0}",
            "const z=()=>1;",
            "def x(a,b):return a+b",
            "a=1;b=2;c=3",
            "function z(){return 0}",
            "x=5",
        ]
        all_codes = good + bad
        labels = [1] * len(good) + [0] * len(bad)
        X = np.array([self.extract_features(c) for c in all_codes])
        y = np.array(labels)
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        self.quality_classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.quality_classifier.fit(X_train, y_train)
        y_pred = self.quality_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        feature_names = ['length','lines','def_count','import_count','print_count','self_count','colons','hash_comments','function_count','const_count','console_log','arrows','semicolons','braces','html_open','html_close','doctype','html_tags','css_props','hex_colors','css_classes','media_queries','md_headings','md_bold','md_links','md_lists']
        importances = self.quality_classifier.feature_importances_
        top = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:5]
        joblib.dump(self.quality_classifier, os.path.join(self.model_path, 'quality_classifier.pkl'))
        return {'accuracy': round(accuracy * 100, 2), 'training_samples': len(X_train), 'test_samples': len(X_test), 'top_features': [{'feature': f, 'importance': round(i * 100, 2)} for f, i in top]}
    
    def predict_quality(self, code):
        model_file = os.path.join(self.model_path, 'quality_classifier.pkl')
        if os.path.exists(model_file):
            self.quality_classifier = joblib.load(model_file)
        else:
            return {'error': 'Quality model not trained yet'}
        vector = np.array(self.extract_features(code)).reshape(1, -1)
        proba = self.quality_classifier.predict_proba(vector)[0]
        score = round(proba[1] * 100, 2)
        label = 'good' if score > 60 else 'poor'
        if score > 80:
            rec = 'Excellent code quality.'
        elif score > 60:
            rec = 'Good code. Minor improvements possible.'
        elif score > 40:
            rec = 'Fair code. Add comments and better names.'
        else:
            rec = 'Poor code. Needs refactoring.'
        return {'quality_score': score, 'label': label, 'recommendation': rec}
    
    def get_sample_training_data(self):
        py = [
            "def hello():\n    print('Hello')\n\nclass MyClass:\n    def method(self):\n        return 1",
            "import os\nimport sys\n\ndef main():\n    for i in range(10):\n        print(i)",
            "class BankAccount:\n    def __init__(self, balance):\n        self.balance = balance",
            "def fib(n):\n    if n <= 1:\n        return n\n    return fib(n-1) + fib(n-2)",
            "import json\nimport requests\n\ndef fetch(url):\n    r = requests.get(url)\n    return json.loads(r.text)",
            "def quicksort(arr):\n    if len(arr) <= 1:\n        return arr\n    pivot = arr[0]",
            "class Node:\n    def __init__(self, value):\n        self.value = value",
            "def deco(func):\n    def wrap(*args):\n        return func(*args)\n    return wrap",
        ]
        js = [
            "function hello() {\n    console.log('Hello');\n}\n\nclass MyClass {\n    method() { return 1; }\n}",
            "const express = require('express');\nconst app = express();\napp.get('/', (req, res) => res.send('Hello'));",
            "import React from 'react';\nfunction App() {\n    return <div>Hello</div>;\n}\nexport default App;",
            "const numbers = [1,2,3,4,5];\nconst doubled = numbers.map(n => n * 2);",
            "async function fetchData() {\n    const r = await fetch('https://api.com');\n    return r.json();\n}",
            "function total(items) {\n    let sum = 0;\n    for (let i = 0; i < items.length; i++) { sum += items[i]; }\n    return sum;\n}",
            "const person = { name: 'John', age: 30 };",
            "export default class Component {\n    constructor(props) { this.props = props; }\n}",
        ]
        html = [
            "<!DOCTYPE html>\n<html>\n<head><title>Page</title></head>\n<body><h1>Hello</h1></body>\n</html>",
            "<div class='container'>\n    <p>Text</p>\n    <a href='#'>Link</a>\n</div>",
            "<form action='/submit' method='POST'>\n    <input type='text' name='user'>\n    <button>Submit</button>\n</form>",
            "<table>\n    <tr><th>Name</th></tr>\n    <tr><td>John</td></tr>\n</table>",
        ]
        css = [
            "body { font-family: Arial; margin: 0; background: #fff; }",
            ".container { max-width: 1200px; margin: 0 auto; padding: 20px; }",
            ".header { background: #333; color: white; padding: 15px; }",
            ".btn { padding: 10px 20px; border-radius: 5px; }",
            "@media (max-width: 768px) { .container { padding: 10px; } }",
        ]
        md = [
            "# Project Title\n\n## Description\nThis is a project.\n\n## Install\n```\nnpm install\n```",
            "## Features\n- Feature 1\n- Feature 2\n\n## Usage\nSee docs.",
            "# Heading\n\nSome **bold** and *italic* text.\n\n![Image](url)",
            "## Table\n| Col 1 | Col 2 |\n|-------|-------|\n| Data | Data |",
        ]
        samples = py + js + html + css + md
        labels = ['python']*len(py) + ['javascript']*len(js) + ['html']*len(html) + ['css']*len(css) + ['markdown']*len(md)
        return samples, labels