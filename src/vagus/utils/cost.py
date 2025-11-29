import sys
completion_cost = None # Initialize for explicit checking

try:
    from litellm import completion_cost
except ImportError:
    # completion_cost remains None if litellm is not available
    pass

def print_cost(model_name, messages, completion_text):
    """
    Calculates and prints the estimated cost of the transaction to stderr.
    Uses ANSI escape codes to print in dim gray so it dosen't distract.
    Returns the cost as a float, or None if calculation fails or litellm is missing.
    """
    if completion_cost is None:
        return None
    try:
        cost = completion_cost(
                model=model_name,
                messages=messages,
                completion=completion_text
        )

        print(f"\033[90m[Cost: ${cost:.6f}]\033[0m", file=sys.stderr)
        return cost

    except Exception:
        return None
