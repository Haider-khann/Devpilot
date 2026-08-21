with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add CSS and Markdown samples before the return statement
old_return = "        return code_samples, languages"
new_data = '''        css_codes = [
            "body { font-family: Arial; margin: 0; padding: 0; background: #fff; }",
            ".container { max-width: 1200px; margin: 0 auto; padding: 20px; }",
            ".header { background: #333; color: white; padding: 15px; }",
            ".btn { padding: 10px 20px; border-radius: 5px; cursor: pointer; }",
            "@media (max-width: 768px) { .container { padding: 10px; } }",
            ".card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.1); transform: translateY(-2px); }",
        ]
        
        md_codes = [
            "# Project Title\\n\\n## Description\\nThis is a project.\\n\\n## Installation\\n```\\nnpm install\\n```",
            "## Features\\n- Feature 1\\n- Feature 2\\n\\n## Usage\\nSee documentation.",
            "# Heading\\n\\nSome text with **bold** and *italic*.\\n\\n![Image](url)",
            "## Table\\n| Column 1 | Column 2 |\\n|----------|----------|\\n| Data 1 | Data 2 |",
        ]
        
        code_samples = python_codes + js_codes + html_codes + css_codes + md_codes
        languages = (['python'] * len(python_codes) + 
                    ['javascript'] * len(js_codes) + 
                    ['html'] * len(html_codes) +
                    ['css'] * len(css_codes) +
                    ['markdown'] * len(md_codes))
        
        return code_samples, languages'''

content = content.replace(old_return, new_data)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Added CSS and Markdown training samples!")