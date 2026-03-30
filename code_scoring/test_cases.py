import multiprocessing
import traceback

multiprocessing.freeze_support()

def evaluate_code(code, test_cases, func_name="add"):
    """
    Evaluates user code and returns score + detailed results
    """

    passed = 0
    total = len(test_cases)
    results = []

    try:
        local_env = {}

        # Execute user code
        exec(code, local_env)

        if func_name not in local_env:
            return 0, ["❌ Function 'add' not found"]

        func = local_env[func_name]

        for i, tc in enumerate(test_cases):

            try:
                result = func(*tc["input"])

                if result == tc["output"]:
                    passed += 1
                    results.append(
                        f"✅ Test Case {i+1} Passed → Input {tc['input']} → Output {result}"
                    )
                else:
                    results.append(
                        f"❌ Test Case {i+1} Failed → Input {tc['input']} → Expected {tc['output']} but got {result}"
                    )

            except Exception as e:
                results.append(
                    f"❌ Test Case {i+1} Error → {str(e)}"
                )

    except Exception:
        return 0, ["❌ Code execution failed"]

    score = (passed / total) * 10 if total > 0 else 0

    return round(score, 2), results
