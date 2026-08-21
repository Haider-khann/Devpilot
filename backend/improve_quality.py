with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Expand good and bad code samples
old_good_start = "good_codes = ["
old_good_end = "]"

new_good = '''good_codes = [
            "def calculate_total(items):\\n    total = 0\\n    for item in items:\\n        total += item.price\\n    return total",
            "class User:\\n    def __init__(self, name):\\n        self.name = name\\n\\n    def greet(self):\\n        return f'Hello, {self.name}'",
            "def fetch_data(url):\\n    try:\\n        response = requests.get(url)\\n        return response.json()\\n    except Exception as e:\\n        print(f'Error: {e}')\\n        return None",
            "function calculateSum(numbers) {\\n    return numbers.reduce((sum, num) => sum + num, 0);\\n}",
            "const validateEmail = (email) => {\\n    const regex = /^[^\\\\s@]+@[^\\\\s@]+\\\\.[^\\\\s@]+$/;\\n    return regex.test(email);\\n};",
            "def calculate_average(numbers):\\n    if not numbers:\\n        return 0\\n    return sum(numbers) / len(numbers)",
            "def is_prime(n):\\n    if n < 2:\\n        return False\\n    for i in range(2, int(n**0.5) + 1):\\n        if n % i == 0:\\n            return False\\n    return True",
            "class BankAccount:\\n    def __init__(self, balance=0):\\n        self.balance = balance\\n\\n    def deposit(self, amount):\\n        if amount > 0:\\n            self.balance += amount\\n            return True\\n        return False",
            "function sortByDate(items) {\\n    return items.sort((a, b) => new Date(b.date) - new Date(a.date));\\n}",
            "const formatPrice = (price) => {\\n    return `$${price.toFixed(2)}`;\\n};",
        ]'''

# Find and replace good_codes section
import re
pattern = r'good_codes = \[.*?\]'
content = re.sub(pattern, new_good, content, count=1, flags=re.DOTALL)

# Expand bad codes
new_bad = '''bad_codes = [
            "def f(x):\\n    return x+1",
            "x=10\\ny=20\\nz=x+y\\nprint(z)",
            "def do_stuff():\\n    pass",
            "function x() { return 1; }",
            "const a = 5; const b = 10; console.log(a + b);",
            "def q():\\n    global x\\n    x = x + 1",
            "a=1\\nb=2\\nc=a+b",
            "def x(a,b):\\n    return a*b",
            "function y(){return 0}",
            "const z=()=>1;",
        ]'''

pattern2 = r'bad_codes = \[.*?\]'
content = re.sub(pattern2, new_bad, content, count=1, flags=re.DOTALL)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Quality model training data expanded!")