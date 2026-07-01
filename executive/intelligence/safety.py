def safe_execute(fn, fallback, label="executive_stage"):
    """
    Prevents single-stage failure from breaking entire executive pipeline.
    """
    try:
        return fn()
    except Exception as e:
        return {
            "error": True,
            "stage": label,
            "message": str(e),
            "fallback": fallback,
        }
