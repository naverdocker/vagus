# Vagus Test Prompts & Scenarios

This document contains a list of commands and prompts to manually verify the functionality of the Vagus CLI tool.

## 1. Basic Connectivity & Response
*Goal: Verify the LLM connects and responds.*
```bash
vagus "What is the capital of France?"
```

## 2. Context & Memory
*Goal: Verify that Vagus remembers the previous turn.*
```bash
# Step 1: Set context
vagus "My name is Alice."

# Step 2: Recall context
vagus "What is my name?"
```

## 3. System Pipes (Stdin Input)
*Goal: Verify Vagus can read input piped from another command.*
```bash
echo "The quick brown fox jumps over the lazy dog" | vagus "Translate this text to Spanish"
```

## 4. JSON Mode (`--json`)
*Goal: Verify the output is valid JSON format.*
```bash
vagus "List 3 fruits and their colors" --json
```
*Expected Output:* A JSON object or array (e.g., `[{"fruit": "Apple", "color": "Red"}, ...]`).

## 5. Streaming vs. No-Streaming (`--no-stream`)
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

## 6. File Redirection & Large Output
*Goal: Verify output integrity when saving to a file.*
```bash
vagus "Generate a CSV file with 100 rows of dummy user data (id, name, email)." --no-stream > test_data.csv
```
*Verification:* Check `test_data.csv` to ensure it has 100+ lines and isn't truncated.

## 7. Code Generation
*Goal: Verify Vagus produces correctly formatted code blocks.*
```bash
vagus "Write a Python function to calculate the Fibonacci sequence recursively."
```

## 8. Temperature Control (`-t`)
*Goal: Verify the temperature parameter affects randomness.*

**Low Temperature (Deterministic):**
```bash
vagus "Pick a random number between 1 and 100" -t 0.0
```

**High Temperature (Creative):**
```bash
vagus "Invent a new word and define it" -t 1.5
```

## 9. Cost Display
*Goal: Verify the cost is printed to stderr (dimmed).*
```bash
vagus "Hello"
```
*Observation:* Look for `[Cost: $0.00...]` in gray at the end of the output.
