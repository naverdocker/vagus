import pytest
from vagus.core.llm import query_model

# Test query_model with streaming enabled
def test_query_model_stream(mocker):
    mock_completion_chunk_1 = mocker.Mock()
    mock_completion_chunk_1.choices = [mocker.Mock()]
    mock_completion_chunk_1.choices[0].delta.content = "Hello"

    mock_completion_chunk_2 = mocker.Mock()
    mock_completion_chunk_2.choices = [mocker.Mock()]
    mock_completion_chunk_2.choices[0].delta.content = ", world!"

    mock_completion_chunk_3 = mocker.Mock()
    mock_completion_chunk_3.choices = [mocker.Mock()]
    mock_completion_chunk_3.choices[0].delta.content = None # End of stream

    mock_completion = mocker.Mock(
        return_value=iter([mock_completion_chunk_1, mock_completion_chunk_2, mock_completion_chunk_3])
    )
    mocker.patch('vagus.core.llm.completion', new=mock_completion)
    mocker.patch('vagus.core.llm.print_cost')

    messages = [{"role": "user", "content": "test"}]
    result = query_model("test-model", messages, stream_output=True)

    assert result == "Hello, world!"
    mock_completion.assert_called_once_with(
        model="test-model", messages=messages, temperature=0.7, stream=True
    )

# Test query_model with streaming disabled
def test_query_model_no_stream(mocker):
    mock_completion_chunk_1 = mocker.Mock()
    mock_completion_chunk_1.choices = [mocker.Mock()]
    mock_completion_chunk_1.choices[0].delta.content = "Hello"

    mock_completion_chunk_2 = mocker.Mock()
    mock_completion_chunk_2.choices = [mocker.Mock()]
    mock_completion_chunk_2.choices[0].delta.content = ", world!"

    mock_completion_chunk_3 = mocker.Mock()
    mock_completion_chunk_3.choices = [mocker.Mock()]
    mock_completion_chunk_3.choices[0].delta.content = None

    mock_completion = mocker.Mock(
        return_value=iter([mock_completion_chunk_1, mock_completion_chunk_2, mock_completion_chunk_3])
    )
    mocker.patch('vagus.core.llm.completion', new=mock_completion)
    mocker.patch('vagus.core.llm.print_cost')

    messages = [{"role": "user", "content": "test"}]
    result = query_model("test-model", messages, stream_output=False)

    assert result == "Hello, world!"
    mock_completion.assert_called_once_with(
        model="test-model", messages=messages, temperature=0.7, stream=True
    )
