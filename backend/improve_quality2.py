with open('ml_service.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Add more good code examples
old_good = '"const formatPrice = (price) => {\n    return `$${price.toFixed(2)}`;\n};"'
new_good = '"const formatPrice = (price) => {\n    return `$${price.toFixed(2)}`;\n};",\n            "def read_file(filepath):\n    with open(filepath, \'r\') as file:\n        return file.read()",\n            "def write_file(filepath, content):\n    with open(filepath, \'w\') as file:\n        file.write(content)",\n            "class Rectangle:\n    def __init__(self, width, height):\n        self.width = width\n        self.height = height\n\n    def area(self):\n        return self.width * self.height",\n            "def merge_sort(arr):\n    if len(arr) <= 1:\n        return arr\n    mid = len(arr) // 2\n    left = merge_sort(arr[:mid])\n    right = merge_sort(arr[mid:])\n    return merge(left, right)",\n            "async function getUser(id) {\n    const response = await fetch(`/api/users/${id}`);\n    if (!response.ok) throw new Error(\'Failed\');\n    return response.json();\n}"'

content = content.replace(old_good, new_good)

# Add more bad code examples
old_bad = '"const z=()=>1;"'
new_bad = '"const z=()=>1;",\n            "def x(a,b):return a+b",\n            "a=1;b=2;c=3",\n            "function z(){return 0}",\n            "x=5"'

content = content.replace(old_bad, new_bad)

with open('ml_service.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Training data expanded!")