import ast

def get_code_feedback(code: str):
    """
    Checks syntax errors and basic structure.
    """

    try:
        ast.parse(code)
    except SyntaxError as e:
        return {
            "status": "error",
            "message": f"❌ Syntax Error: {e.msg} (line {e.lineno})"
        }

    feedback = []

    if "def " not in code:
        feedback.append("⚠️ No function defined.")

    if "return" not in code:
        feedback.append("⚠️ Missing return statement.")

    if not feedback:
        message = "✅ Code structure looks good."
    else:
        message = " ".join(feedback)

    return {
        "status": "ok",
        "message": message
    }
