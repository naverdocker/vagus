import sys
import hashlib
import argparse
import os
import logging

import litellm
from litellm.exceptions import AuthenticationError, RateLimitError, APIConnectionError, NotFoundError

from .config import DEFAULT_MODEL, DEFAULT_TEMP
from .memory.storage import load_memory, save_memory
from .core.llm import query_model

os.environ["LITELLM_LOG"] = "CRITICAL"
litellm.suppress_debug_info = True
logging.getLogger("LiteLLM").setLevel(logging.CRITICAL)
logging.getLogger("litellm").setLevel(logging.CRITICAL)

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

def get_file_hash(file_path):
    """Computes MD5 hash of the file content."""
    hasher = hashlib.md5()
    with open(file_path, 'rb') as f:
        buf = f.read(65536)
        while len(buf) > 0:
            hasher.update(buf)
            buf = f.read(65536)
    return hasher.hexdigest()

def setup_rag_context(file_path, query_text):
    """Initializes vector store, checks cache, ingests if needed, and retrieves context."""
    if not file_path:
        return ""

    try:
        from .memory.vector_store import VectorStore
        from .utils.pdf_ingestor import extract_text_from_pdf, chunk_text

        # Use a persistent collection for file caching
        store = VectorStore(collection_name="vagus_file_cache")

        # 1. Compute Hash
        file_hash = get_file_hash(file_path)

        # 2. Check Cache
        # We query for just 1 ID with this hash to see if it exists
        existing = store.collection.get(where={"file_hash": file_hash}, limit=1)

        if not existing['ids']:
            print(f"[RAG] Ingesting new file: {file_path}...", file=sys.stderr)
            raw_text = extract_text_from_pdf(file_path)
            chunks = chunk_text(raw_text)
            # Tag chunks with the hash so we can find them later
            store.add_documents(chunks, metadatas=[{"file_hash": file_hash}] * len(chunks))
        else:
            print(f"[RAG] Using cached embeddings for {file_path}", file=sys.stderr)

        # 3. Retrieve (Filtered by Hash)
        results = store.query([query_text], n_results=3, where={"file_hash": file_hash})

        if results and results['documents'] and results['documents'][0]:
            return "\n\n[Relevant Documents (RAG)]:\n" + "\n".join(results['documents'][0])

    except ImportError:
        print("\nError: RAG deps missing. Run 'pip install vagus[rag]'\n", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nRAG Error: {e}", file=sys.stderr)
        sys.exit(1)

    return ""

def entry_point():
    """The main execution flow."""
    parser = argparse.ArgumentParser(description="vagus: The Neural Interface")
    parser.add_argument("prompt", nargs="*", help="The user prompt")
    parser.add_argument("-m", "--model", type=str, default=DEFAULT_MODEL, help="Model name")
    parser.add_argument("-t", "--temp", type=float, default=DEFAULT_TEMP, help="Temperature")
    parser.add_argument("-s", "--session", type=str, help="Session name")
    parser.add_argument("--rag", type=str, help="Path to PDF file for context")
    parser.add_argument("--json", action="store_true", help="Force JSON output")
    parser.add_argument("--no-stream", action="store_true", help="Disable Streaming")
    args = parser.parse_args()

    try:
        final_user_input = get_user_input(args)
        rag_context = setup_rag_context(args.rag, final_user_input)
        history = load_memory(session=args.session)

        messages = history + [{"role": "user", "content": final_user_input}]

        sys_content = "You are Vagus, a command-line AI interface. Be concise and technically accurate."
        if args.json:
            sys_content += " Output only valid JSON."

        if rag_context:
            sys_content += f"\n\nUse the following retrieved context to answer the user:\n{rag_context}"

        messages.insert(0, {"role": "system", "content": sys_content})

        stream_enabled = not args.no_stream
        response_text = query_model(args.model, messages, args.temp, stream_output=stream_enabled)

        if args.no_stream:
            print(response_text)

        save_memory(final_user_input, response_text, session=args.session)

    except KeyboardInterrupt:
        print("\n\n[Signal Lost]", file=sys.stderr)
        sys.exit(0)
    except AuthenticationError:
        print(f"\nError: Authentication Failed for model '{args.model}'.", file=sys.stderr)
        sys.exit(1)
    except RateLimitError:
        print(f"\nError: Rate Limit Exceeded.", file=sys.stderr)
        sys.exit(1)
    except NotFoundError:
        print(f"\nError: Model '{args.model}' not found.", file=sys.stderr)
        sys.exit(1)
    except APIConnectionError:
        print(f"\nError: Connection Failed.", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {e}", file=sys.stderr)
        sys.exit(1)

if __name__ == "__main__":
    entry_point()