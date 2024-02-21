import ollama


class OLLMClient:
    def __init__(self, model_name='mistral', role='user'):
        self.model_name = model_name
        self.role = role
        self.format = 'json'  # Currently the only accepted value is json

    def send_request(self, message_content):
        stream = ollama.chat(
            model=self.model_name,
            messages=[{'role': self.role, 'content': message_content}]
        )
        # Assuming the stream object can be iterated to get responses
        responses = [response for response in stream]
        return responses

    def set_model(self, model_name):
        self.model_name = model_name
