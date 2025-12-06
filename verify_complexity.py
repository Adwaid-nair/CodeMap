import radon.complexity as radon_cc
from radon.visitors import ComplexityVisitor

file_path = "c:\\AntiGravity L\\space_adventure.py"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Calculate complexity as done in python_analyzer.py
cv = ComplexityVisitor.from_code(content)
file_cc = sum([f.complexity for f in cv.functions]) + (cv.complexity if hasattr(cv, 'complexity') else 0)

print(f"File: {file_path}")
print(f"Total Complexity: {file_cc}")

for f in cv.functions:
    print(f"Function {f.name}: {f.complexity}")
