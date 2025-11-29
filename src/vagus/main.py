import sys
import argparse
from .config import DEFAULT_MODEL, DEFAULT_TEMP
from .memory.storage import load_memory, save_memory
from .core.llm import query_model

def get_user_input(args):
    """Combines command line arguments and piped stdin into a single prompt."""
    parts = []

    if args.prompt:
        parts.append(" ".join(args.prompt))

    if not sys.stdin.isatty():
        piped_data = sys.stdin.read().strip()
        if piped_data:
            parts.append(f"\n[Context Data]:\n{piped_data}")

    if not parts:
        print("Usage: vagus 'prompt' | vagus -m gpt-4 'prompt'", file=sys.stderr)
        sys.exit(1)

    return "\n".join(parts)


def entry_point():
    """The main execution flow."""
    # --- ARGUMENT PARSING ---
    parser = argparse.ArgumentParser(description="vagus: The Neural Interface")
    parser.add_argument("prompt", nargs="*", help="The user prompt")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("-t", "--temp", type=str, default=DEFAULT_TEMP, help="Temperature")
    parser.add_argument("--json", action="store_true", help="Force JSON output")
    args = parser.parse_args()


    try:
        # --- PREPARE CONTEXT ---
        final_user_input = get_user_input(args)
        history = load_memory()

        messages = history + [{"role": "user", "content": final_user_input}]

        # System Prompt
        sys_content = "You are Vagus, a digital regulatory system. Be concise."
        if args.json:
            sys_content += " Output only valid JSON."
        messages.insert(0, {"role": "system", "content": sys_content})


        # --- CALL LLM ---
        response_text = query_model(args.model, messages, args.temp)


        # --- PERSIST MEMORY ---
        save_memory(final_user_input, response_text)

    except KeyboardInterrupt:
        print("\n\n[Signal Lost]", file=sys.stderr)
        sys.exit(0)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    entry_point()
