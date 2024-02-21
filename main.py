import ollama


if __name__ == '__main__':
    stream = ollama.chat(
        model='llama2',
        messages=[{'role': 'user', 'content': 'Why is the sky blue?'}]
    )

    print(stream['message']['content'])