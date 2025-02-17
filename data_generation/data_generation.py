import random
from openai import OpenAI

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

def random_topic(topic_list):
    n = len(topic_list)
    i = random.randint(0,n-1)
    return topic_list[i]
    


if __name__ == "__main__":
    api_key = "YOUR_API_KEY"
    model_name = 'gpt-4o-mini'
    client = OpenAI(api_key=api_key)
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
        output = OpenAIGPT(client,model_name,prompt)
        print(output)        
        with open(f"data/example{i}.txt", "w") as file:
            file.write(output)
















