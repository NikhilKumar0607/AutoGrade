import ast

def code_quality_score(code):
    tree = ast.parse(code)

    lines = code.strip().split("\n")
    total_lines = len(lines)
    comment_lines = sum(1 for line in lines if line.strip().startswith("#"))

    functions = sum(isinstance(node, ast.FunctionDef) for node in ast.walk(tree))

    # Simple scoring logic
    score = 10

    if total_lines > 50:
        score -= 2
    if functions == 0:
        score -= 3
    if comment_lines == 0:
        score -= 2

    return max(score, 0)


# TESTING
if __name__ == "__main__":
    sample_code = """
# Adds two numbers
def solution(a, b):
    return a + b
"""

    quality = code_quality_score(sample_code)
    print("Code Quality Score:", quality)
