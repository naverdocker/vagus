import sys
from litellm import completion

from ..utils.cost import print_cost

def query_model(model_name, messages, temperature=0.7, stream_output=True):
    """
    Streams the response from the llm.
    Return the full aggregated response text after streaming.
    """
    full_response_text = ""

    response = completion(
            model=model_name,
            messages=messages,
            temperature=temperature,
            stream=True
    )

    for chunk in response:
        if chunk.choices and chunk.choices[0].delta.content:
            delta = chunk.choices[0].delta.content
            if stream_output:
                print(delta, end="", flush=True)
            full_response_text += delta

    if stream_output:
        print()

    print_cost(model_name, messages, full_response_text)

    return full_response_text
