import sys

try:
    from litellm import completion
except ImportError:
    print("Error: 'litellm' module not found." file=sys.stderr)
    sys.exit(1)

def query_model(model_name, messages, temperature=0.7):
    full_text_response = ""

    try:
        reponse = completion(
                model=model_name,
                messages=messages,
                temperature=temperature,
                stream=True
        )

        for chunk in response:
            if chunk.choices and chunk.choices[0].delta.content:
                delta = chunk.choices[0].delta.content
                print(delta, end="", flush=True)
                full_response_text += delta

        print()
        return full_response_text

    except Exception as e:
        raise Exception(f"Signal blocked - {srt(e)}")
