import random
from openai import OpenAI

DEFAULT_KEY = "YOUR_API_KEY"
def OpenAIGPT(client,model_name,content):
    completion = client.chat.completions.create(
    model=model_name,
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": content
        }
    ]
    )
    return completion.choices[0].message.content

class DeepSeekAgent():
    def __init__(self, model_name='deepseek-chat', api_key=None, base_url="https://api.deepseek.com"):
        if api_key is None:
            api_key=DEFAULT_KEY
        self.client = OpenAI(api_key=api_key,base_url=base_url)
        self.model_name = model_name
        self.reset()
    
    def query(self, prompt, reset=False):
        if reset:
            self.reset()
        self.history.append({"role":"user", "content": prompt})
        completion = self.client.chat.completions.create(
            model=self.model_name,
            messages=self.history
        )
        content = completion.choices[0].message.content
        self.history.append({"role":"assistant", "content": content})
        return content

    def reset(self):
        self.history = [{"role": "system", "content": "You are a helpful assistant."}]
def random_topic(topic_list):
    n = len(topic_list)
    i = random.randint(0,n-1)
    return topic_list[i]
    


if __name__ == "__main__":
    api_key = DEFAULT_KEY#"YOUR_API_KEY"
    model_name = 'deepseek-chat'
    model = DeepSeekAgent(model_name,api_key)
    prompt = "Who is Messi?"
    print(model.query(prompt, reset=True))
    