from openai import OpenAI
from config import config 

class OpenAIClient:
    def __init__(self, model, temperature, json_object):
        
        self.messages = []
        self.client = OpenAI(api_key=config.OPENAI_API_KEY)
        self.model = model
        self.temperature = temperature
        if json_object:
            self.response_format = {"type": "json_object"}
        else:
            self.response_format = {"type": "text"}


    def completions(self):
        response = self.client.chat.completions.create(
            model=self.model,
            temperature=self.temperature,
            response_format=self.response_format,
            messages=self.messages
        )
    
        return response.choices[0].message.content, response.usage
    
    def add_to_message(self, content, role):
        """
        Adds a new message to the message list.

        :param content: The content of the message.
        :param role: The role of the message sender ('user', 'assistant' or 'system').
        """
        message = {"role": role, "content": content}
        if content:
            self.messages.append(message)

