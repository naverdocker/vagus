import sys
import os
import json
import unittest
from unittest.mock import patch, MagicMock
from vagus.main import entry_point
import vagus.memory.storage

# Mock object for litellm response
class MockChunk:
    def __init__(self, content):
        self.choices = [MagicMock()]
        self.choices[0].delta.content = content

class TestVagus(unittest.TestCase):
    def setUp(self):
        # Use a temporary file for memory
        self.test_memory_file = "tests/test_memory.jsonl"
        if os.path.exists(self.test_memory_file):
            os.remove(self.test_memory_file)
        
        # Patch the MEMORY_FILE in the storage module
        self.memory_patcher = patch('vagus.memory.storage.MEMORY_FILE', self.test_memory_file)
        self.memory_patcher.start()

    def tearDown(self):
        self.memory_patcher.stop()
        if os.path.exists(self.test_memory_file):
            os.remove(self.test_memory_file)

    @patch('vagus.core.llm.print_cost')
    @patch('vagus.core.llm.completion')
    def test_entry_point_flow(self, mock_completion, mock_print_cost):
        # Setup mock response
        mock_completion.return_value = [
            MockChunk("Hello "),
            MockChunk("World"),
            MockChunk("!")
        ]

        # Mock command line arguments
        test_args = ["vagus", "Hello", "Computer"]
        
        # Capture stdout
        from io import StringIO
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(sys, 'argv', test_args):
                entry_point()
            
            output = fake_out.getvalue()
            self.assertIn("Hello World!", output)

        # Verify memory file was created and content is correct
        self.assertTrue(os.path.exists(self.test_memory_file), "Memory file should exist")
        
        with open(self.test_memory_file, 'r') as f:
            lines = f.readlines()
            self.assertEqual(len(lines), 1, "Should have one memory entry")
            entry = json.loads(lines[0])
            self.assertEqual(entry['input'], "Hello Computer")
            self.assertEqual(entry['output'], "Hello World!")

    @patch('vagus.core.llm.print_cost')
    @patch('vagus.core.llm.completion')
    def test_entry_point_no_stream(self, mock_completion, mock_print_cost):
        # Setup mock response
        mock_completion.return_value = [
            MockChunk("Test "),
            MockChunk("No "),
            MockChunk("Stream")
        ]

        # Mock command line arguments with --no-stream
        test_args = ["vagus", "Testing", "--no-stream"]
        
        # Capture stdout
        from io import StringIO
        with patch('sys.stdout', new=StringIO()) as fake_out:
            with patch.object(sys, 'argv', test_args):
                entry_point()
            
            output = fake_out.getvalue()
            # Verify full output is present (newlines might vary, so strip)
            self.assertIn("Test No Stream", output)

        # Verify memory
        with open(self.test_memory_file, 'r') as f:
            lines = f.readlines()
            entry = json.loads(lines[0])
            self.assertEqual(entry['output'], "Test No Stream")

if __name__ == '__main__':
    unittest.main()
