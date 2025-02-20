import random
from openai import OpenAI

DEFAULT_KEY = "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"
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

class OpenAIAgent():
    def __init__(self, model_name='gpt-4o-mini', api_key=None):
        if api_key is None:
            api_key=DEFAULT_KEY
        self.client = OpenAI(api_key=api_key)
        self.model_name = model_name
        self.reset()
    
    def query(self, prompt, reset=False):
        if reset:
            self.reset()
        self.history.append({"role":"user", "content": prompt})
        completion = client.chat.completions.create(
            model=model_name,
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
    api_key = None#"YOUR_API_KEY"
    model_name = 'gpt-4o-mini'
    model = OpenAIAgent(model_name,api_key)
    topic_list = ["work",'family','school','relationship','hobbies']
    for i in range(1,2):
        print("satrt")
        topic = random_topic(topic_list)
        print("Topic:",topic)
        prompt = f"Please generate a 20-round dialogue with the following requirements:\
                   1. The conversation should involve emotional care between both parties.\
                   2. The topic is related to {topic}" + \
                   "3. The final round\'s question must be closely related to the initial conversation, and the response should specifically reference details from the beginning.\
                    Return only the formatted dialogue without additional explanations. \
                    The format should be one line for one conversation: \"conversation1 \n conversation2 \n...\". No other explanation!"
        output = model(prompt)
        print(output)        
        with open(f"data/example{i}.txt", "w") as file:
            file.write(output)