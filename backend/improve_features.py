with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add more distinguishing features
old_features = """    def extract_features(self, code):
        return [
            len(code),
            len(code.splitlines()),
            len(re.findall(r'\\bdef\\b|\\bfunction\\b', code)),
            len(re.findall(r'\\bclass\\b', code)),
            len(re.findall(r'\\bimport\\b|\\brequire\\b|\\binclude\\b', code)),
            len(re.findall(r'[{}]', code)),
            code.count(';'),
            code.count(':'),
            len(re.findall(r'->|=>', code)),
            len(re.findall(r'#', code)),
            len(re.findall(r'//', code)),
            len(re.findall(r'\\bprint\\b|\\bconsole\\.log\\b', code)),
            len(re.findall(r'<[a-z]+>', code)),
        ]"""

new_features = """    def extract_features(self, code):
        return [
            len(code),
            len(code.splitlines()),
            # Python indicators
            len(re.findall(r'\\bdef\\b', code)),
            len(re.findall(r'\\bimport\\s+\\w+', code)),
            len(re.findall(r'\\bprint\\s*\\(', code)),
            len(re.findall(r'\\bself\\b', code)),
            code.count(':'),
            len(re.findall(r'#.*', code)),
            # JavaScript indicators
            len(re.findall(r'\\bfunction\\b', code)),
            len(re.findall(r'\\bconst\\b|\\blet\\b|\\bvar\\b', code)),
            len(re.findall(r'console\\.log', code)),
            len(re.findall(r'=>', code)),
            code.count(';'),
            len(re.findall(r'[{}]', code)),
            # HTML indicators
            len(re.findall(r'<[a-z]+[^>]*>', code)),
            len(re.findall(r'</[a-z]+>', code)),
            len(re.findall(r'<!DOCTYPE', code, re.IGNORECASE)),
            len(re.findall(r'<html|<head|<body|<div|<p|<span', code)),
            # CSS indicators
            len(re.findall(r'[a-z-]+\\s*:\\s*[^;]+;', code)),
            len(re.findall(r'#[a-fA-F0-9]{3,6}', code)),
            len(re.findall(r'\\.[a-z-]+\\s*{', code)),
            len(re.findall(r'@media|@import', code)),
            # Markdown indicators
            len(re.findall(r'^#{1,6}\\s', code, re.MULTILINE)),
            len(re.findall(r'\\*\\*.*\\*\\*', code)),
            len(re.findall(r'\\[.*\\]\\(.*\\)', code)),
            len(re.findall(r'^[-*]\\s', code, re.MULTILINE)),
        ]"""

content = content.replace(old_features, new_features)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Feature extraction improved - now 26 features!")