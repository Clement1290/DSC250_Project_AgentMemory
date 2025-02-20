# %%
import os
from ollama import chat, Client


class OllamaAgent():
    def __init__(self, model_name='qwen2.5:3b'):
        os.system("ollama serve")
        self.model_name = model_name
        self.reset()
    def query(self, prompt, reset=False):
        if reset:
            self.reset()
        self.history.append({"role": "user", "content": prompt})
        response = chat(model=self.model_name, messages=self.history)
        self.history.append(response['message'])
        return response['message']['content']

    def reset(self):
        self.history = [{"role": "system", "content": "You are a helpful assistant."}]



if __name__ == '__main__':
    agent = OllamaAgent()
    print(agent.query("What is the capital of France?"))
    print(agent.query("What are some famous tourist attraction in the city mentioned above?"))

# %%
