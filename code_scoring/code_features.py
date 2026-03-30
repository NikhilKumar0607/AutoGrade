import ast

def code_quality_score(code):
    try:
        tree = ast.parse(code)
    except:
        # If code has syntax error, return very low score
        return 2

    lines = code.strip().split("\n")
    total_lines = len(lines)

    comment_lines = sum(
        1 for line in lines if line.strip().startswith("#")
    )

    functions = sum(
        isinstance(node, ast.FunctionDef) for node in ast.walk(tree)
    )

    score = 10

    # Penalize very long code
    if total_lines > 50:
        score -= 2

    # Penalize if no functions used
    if functions == 0:
        score -= 3

    # Penalize if no comments
    if comment_lines == 0:
        score -= 1

    return max(score, 0)
