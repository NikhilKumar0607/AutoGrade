import multiprocessing
import traceback


def _run_user_code(code, func_name, args, expected, q):
    """
    Runs user code safely in a separate process.
    Returns pass/fail result in queue.
    """
    try:
        local_env = {}
        exec(code, {}, local_env)

        if func_name not in local_env:
            q.put({"status": "error", "message": f"Function '{func_name}' not found in your code."})
            return

        func = local_env[func_name]
        output = func(*args)

        if output == expected:
            q.put({"status": "ok", "passed": True})
        else:
            q.put({"status": "ok", "passed": False, "got": output, "expected": expected})

    except Exception as e:
        q.put({"status": "error", "message": str(e), "trace": traceback.format_exc()})


def evaluate_code(code, test_cases, func_name="add", timeout=2):
    """
    Evaluates code using test cases with timeout.
    timeout = seconds per test case
    """
    passed = 0
    total = len(test_cases)

    for tc in test_cases:
        q = multiprocessing.Queue()
        p = multiprocessing.Process(
            target=_run_user_code,
            args=(code, func_name, tc["input"], tc["output"], q)
        )

        p.start()
        p.join(timeout)

        # Timeout happened
        if p.is_alive():
            p.terminate()
            p.join()
            continue

        # Read result
        if not q.empty():
            res = q.get()
            if res.get("status") == "ok" and res.get("passed") is True:
                passed += 1

    # score out of 10
    return (passed / total) * 10 if total > 0 else 0
