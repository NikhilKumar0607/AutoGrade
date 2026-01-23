import ast
import traceback

def check_code_errors(code: str):
    """
    Returns:
    (status, message)
    status = "ok" | "syntax_error" | "runtime_error"
    """
    try:
        # Syntax check
        ast.parse(code)
        return "ok", "No Syntax Errors Found"
    except SyntaxError as e:
        return "syntax_error", f"❌ Syntax Error: {e.msg} (line {e.lineno})"
    except Exception as e:
        return "runtime_error", f"❌ Error while parsing code: {str(e)}"


def get_code_feedback(code: str):
    status, msg = check_code_errors(code)

    feedback = {
        "status": status,
        "message": msg
    }

    return feedback
