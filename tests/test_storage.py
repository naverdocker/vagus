import pytest
import os
import json
from vagus.memory.storage import load_memory, save_memory
import vagus.config
import vagus.memory.storage

@pytest.fixture
def temp_memory_setup(tmp_path, mocker):
    # Create temporary paths for memory and sessions
    temp_vagus_dir = tmp_path / ".vagus"
    temp_vagus_dir.mkdir()
    temp_default_memory_file = temp_vagus_dir / "memory.jsonl"
    temp_sessions_dir = temp_vagus_dir / "sessions"
    temp_sessions_dir.mkdir()

    # Patch the config variables directly in vagus.config
    mocker.patch.object(vagus.config, 'VAGUS_DIR', temp_vagus_dir)
    mocker.patch.object(vagus.config, 'DEFAULT_MEMORY_FILE', temp_default_memory_file)
    mocker.patch.object(vagus.config, 'SESSIONS_DIR', temp_sessions_dir)
    mocker.patch.object(vagus.config, 'INTERACTION_WINDOW', 5) # Ensure it's reset for each test

    # Additionally, patch the variables *within the vagus.memory.storage module*
    # because they were imported at module load time.
    mocker.patch.object(vagus.memory.storage, 'DEFAULT_MEMORY_FILE', temp_default_memory_file)
    mocker.patch.object(vagus.memory.storage, 'SESSIONS_DIR', temp_sessions_dir)
    mocker.patch.object(vagus.memory.storage, 'INTERACTION_WINDOW', 5) # Reset here too

    # Yield the default memory file path to the tests
    yield temp_default_memory_file

    # Clean up


def test_save_and_load_memory(temp_memory_setup):
    user_input = "Hello AI"
    assistant_output = "Hello User"

    save_memory(user_input, assistant_output)
    loaded_memory = load_memory()

    expected_history = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": assistant_output}
    ]
    assert loaded_memory == expected_history

def test_load_empty_memory(temp_memory_setup):
    if temp_memory_setup.exists():
        temp_memory_setup.unlink()

    loaded_memory = load_memory()
    assert loaded_memory == []

def test_memory_window_limit(temp_memory_setup, mocker):
    mocker.patch('vagus.config.INTERACTION_WINDOW', 2)
    mocker.patch('vagus.memory.storage.INTERACTION_WINDOW', 2)

    save_memory("u1", "a1")
    save_memory("u2", "a2")
    save_memory("u3", "a3")

    loaded_memory = load_memory()

    expected_history = [
        {"role": "user", "content": "u2"},
        {"role": "assistant", "content": "a2"},
        {"role": "user", "content": "u3"},
        {"role": "assistant", "content": "a3"}
    ]
    assert loaded_memory == expected_history
    assert len(loaded_memory) == 4 # 2 interactions * 2 messages each

def test_save_and_load_session_memory(temp_memory_setup, mocker):
    session_name = "test_session"
    session_file_path = vagus.config.SESSIONS_DIR / f"{session_name}.jsonl"

    user_input = "Session Hello"
    assistant_output = "Session Response"

    save_memory(user_input, assistant_output, session=session_name)
    loaded_memory = load_memory(session=session_name)

    expected_history = [
        {"role": "user", "content": user_input},
        {"role": "assistant", "content": assistant_output}
    ]
    assert loaded_memory == expected_history
    assert session_file_path.exists()

