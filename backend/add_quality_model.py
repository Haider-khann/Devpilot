with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add quality prediction methods before get_sample_training_data
old = "    def get_sample_training_data(self):"
new = """    def train_quality_model(self):
        \"\"\"Train a model to predict code quality.\"\"\"
        # Training data: code features labeled as good (1) or bad (0)
        good_codes = [
            "def calculate_total(items):\\n    total = 0\\n    for item in items:\\n        total += item.price\\n    return total",
            "class User:\\n    def __init__(self, name):\\n        self.name = name\\n\\n    def greet(self):\\n        return f'Hello, {self.name}'",
            "def fetch_data(url):\\n    try:\\n        response = requests.get(url)\\n        return response.json()\\n    except Exception as e:\\n        print(f'Error: {e}')\\n        return None",
            "function calculateSum(numbers) {\\n    return numbers.reduce((sum, num) => sum + num, 0);\\n}",
            "const validateEmail = (email) => {\\n    const regex = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/;\\n    return regex.test(email);\\n};",
        ]
        
        bad_codes = [
            "def f(x):\\n    return x+1",
            "x=10\\ny=20\\nz=x+y\\nprint(z)",
            "def do_stuff():\\n    pass",
            "function x() { return 1; }",
            "const a = 5; const b = 10; console.log(a + b);",
            "def q():\\n    global x\\n    x = x + 1",
        ]
        
        all_codes = good_codes + bad_codes
        labels = [1] * len(good_codes) + [0] * len(bad_codes)
        
        X = np.array([self.extract_features(c) for c in all_codes])
        y = np.array(labels)
        
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)
        
        self.quality_classifier = RandomForestClassifier(n_estimators=50, random_state=42)
        self.quality_classifier.fit(X_train, y_train)
        
        y_pred = self.quality_classifier.predict(X_test)
        accuracy = accuracy_score(y_test, y_pred)
        
        # Feature importance
        feature_names = [
            'length', 'lines', 'def_count', 'import_count', 'print_count',
            'self_count', 'colons', 'hash_comments', 'function_count',
            'const_count', 'console_log', 'arrows', 'semicolons', 'braces',
            'html_open', 'html_close', 'doctype', 'html_tags',
            'css_props', 'hex_colors', 'css_classes', 'media_queries',
            'md_headings', 'md_bold', 'md_links', 'md_lists'
        ]
        importances = self.quality_classifier.feature_importances_
        top_features = sorted(zip(feature_names, importances), key=lambda x: x[1], reverse=True)[:5]
        
        joblib.dump(self.quality_classifier, os.path.join(self.model_path, 'quality_classifier.pkl'))
        
        return {
            'accuracy': round(accuracy * 100, 2),
            'training_samples': len(X_train),
            'test_samples': len(X_test),
            'top_features': [{'feature': f, 'importance': round(i * 100, 2)} for f, i in top_features]
        }
    
    def predict_quality(self, code):
        \"\"\"Predict quality score for new code.\"\"\"
        model_file = os.path.join(self.model_path, 'quality_classifier.pkl')
        if os.path.exists(model_file):
            self.quality_classifier = joblib.load(model_file)
        else:
            return {'error': 'Quality model not trained yet'}
        
        vector = np.array(self.extract_features(code)).reshape(1, -1)
        proba = self.quality_classifier.predict_proba(vector)[0]
        quality_score = round(proba[1] * 100, 2)  # Probability of being "good"
        
        label = 'good' if quality_score > 60 else 'poor'
        
        return {
            'quality_score': quality_score,
            'label': label,
            'recommendation': self._get_quality_recommendation(quality_score)
        }
    
    def _get_quality_recommendation(self, score):
        if score > 80:
            return 'Excellent code quality. Well structured and documented.'
        elif score > 60:
            return 'Good code quality. Minor improvements possible.'
        elif score > 40:
            return 'Fair code. Consider adding comments and better naming.'
        else:
            return 'Poor code quality. Needs significant refactoring.'
    
    def get_sample_training_data(self):"""

content = content.replace(old, new)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Quality prediction model added!")