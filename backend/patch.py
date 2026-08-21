import re

# Read current file
with open('main.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Find the SecurityAnalyzer scan method and replace with enhanced version
old_patterns = """        patterns = [
            ('critical', 'Hardcoded Secret', r'(?i)(password|secret|api[_-]?key|token)\s*=\s*[\"'][^\"']+[\"']'),
            ('high', 'SQL Injection', r'(?i)(execute|cursor\.execute)\s*\(.*f[\"']'),
            ('high', 'Command Injection', r'(?i)(os\.system|subprocess\.(call|run|Popen)|eval|exec)\(),
            ('medium', 'Debug Mode', r'(?i)debug\s*=\s*True'),
            ('medium', 'Insecure Deserialization', r'(?i)(pickle\.loads|yaml\.load\()'),
            ('low', 'Bare Except', r'except\s*:'),
            ('low', 'TODO Comment', r'#\s*TODO'),
        ]"""

new_patterns = """        patterns = [
            ('critical', 'Hardcoded Secret', r'(?i)(password|secret|api[_-]?key|token|auth[_-]?token)\s*=\s*[\"'][^\"']+[\"']'),
            ('critical', 'AWS Key', r'(?i)(aws[_-]?(access|secret)[_-]?key|AKIA[0-9A-Z]{16})'),
            ('high', 'SQL Injection', r'(?i)(execute|cursor\.execute|raw)\s*\(.*f[\"']'),
            ('high', 'Command Injection', r'(?i)(os\.system|subprocess\.(call|run|Popen)|eval|exec|shell=True)\('),
            ('high', 'XSS Vulnerability', r'(?i)(innerHTML|document\.write|dangerouslySetInnerHTML)'),
            ('medium', 'Debug Mode', r'(?i)debug\s*=\s*True'),
            ('medium', 'Insecure Deserialization', r'(?i)(pickle\.loads|yaml\.load\(|json\.loads\()'),
            ('medium', 'Hardcoded URL', r'https?://[a-zA-Z0-9.-]+/[a-zA-Z0-9/_-]*'),
            ('low', 'Bare Except', r'except\s*:'),
            ('low', 'TODO Comment', r'#\s*TODO'),
            ('low', 'Print Statement', r'^\s*print\('),
            ('low', 'Unused Import', r'^\s*import\s+'),
        ]"""

content = content.replace(old_patterns, new_patterns)

with open('main.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Security patterns enhanced!")