# Vagus Test Prompts & Scenarios

This document contains a list of commands and prompts to manually verify the functionality of the Vagus CLI tool.

## Basic Connectivity & Response
*Goal: Verify the LLM connects and responds.*
```bash
vagus "What is the capital of France?"
```

## System Pipes (Stdin Input)
*Goal: Verify Vagus can read input piped from another command.*
```bash
echo "The quick brown fox jumps over the lazy dog" | vagus "Translate this text to Spanish"
```

## JSON Mode (`--json`)
*Goal: Verify the output is valid JSON format.*
```bash
vagus "List 3 fruits and their colors" --json
```
*Expected Output:* A JSON object or array (e.g., `[{"fruit": "Apple", "color": "Red"}, ...]`).

## Streaming vs. No-Streaming (`--no-stream`)
*Goal: Verify the `--no-stream` flag buffers output.*

**Streaming (Default):**
```bash
vagus "Count from 1 to 100 slowly"
```
*Observation:* Numbers should appear one by one (or in chunks).

**No-Streaming:**
```bash
vagus "Count from 1 to 100 slowly" --no-stream
```
*Observation:* The terminal should wait, then print the entire list at once.

## File Redirection & Large Output
*Goal: Verify output integrity when saving to a file.*
```bash
vagus "Generate a CSV file with 100 rows of dummy user data (id, name, email)." --no-stream > test_data.csv
```
*Verification:* Check `test_data.csv` to ensure it has 100+ lines and isn't truncated.

## Code Generation
*Goal: Verify Vagus produces correctly formatted code blocks.*
```bash
vagus "Write a Python function to calculate the Fibonacci sequence recursively."
```

## Temperature Control (`-t`)
*Goal: Verify the temperature parameter affects randomness.*

**Low Temperature (Deterministic):**
```bash
vagus "Pick a random number between 1 and 100" -t 0.0
```

**High Temperature (Creative):**
```bash
vagus "Invent a new word and define it" -t 1.5
```

## Cost Display
*Goal: Verify the cost is printed to stderr (dimmed).*
```bash
vagus "Hello"
```
*Observation:* Look for `[Cost: $0.00...]` in gray at the end of the output.

## Session Management (`--session`)
*Goal: Verify that contexts are isolated.*

**Step 1: Create 'Coding' session**
```bash
vagus --session coding "My favorite language is Python."
```

**Step 2: Create 'Cooking' session**
```bash
vagus --session cooking "My favorite food is Pizza."
```

**Step 3: Verify Isolation**
```bash
vagus --session coding "What is my favorite language?"
# Expect: Python

vagus --session cooking "What is my favorite language?"
# Expect: I don't know (or hallucination, but NOT Python from the other session)
```

## RAG (Chat with Docs)
*Goal: Verify the AI can answer questions based on a provided PDF.*

**Prerequisite:**
Ensure you have installed the RAG dependencies:
```bash
pip install -e .[rag]
```

**Test:**
1. Create a dummy PDF (or use an existing one).
2. Run Vagus pointing to it:
```bash
vagus --rag my_document.pdf "Summarize this document"
```
*Observation:* The output should reflect the specific content of the PDF, not general knowledge.

## Debugging (`--debug`)
*Goal: Verify that the `--debug` flag exposes full tracebacks on error.*

```bash
# Force an error (e.g., by using an invalid model name)
vagus -m invalid-model-name "Hello" --debug
```
*Expected Output:* A full Python traceback should be printed to stderr, followed by the specific error message.

