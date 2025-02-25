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
        completion = self.client.chat.completions.create(
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
    api_key = DEFAULT_KEY#"YOUR_API_KEY"
    model_name = 'gpt-4o-mini'
    model = OpenAIAgent(model_name,api_key)
    topic_list = ["work",'family','school','relationship','hobbies']
    for i in range(1,101):
        print("example: ",i)
        # topic = random_topic(topic_list)
        # print("Topic:",topic)
        prompt_description = f"""Please generate a fake profile of a college student (undergraduate/graduate student) descriptions in the following JSON format without any additional text.\
        [requirements]\
        (1) Include basic information about the person, such as name, age, gender, major, nationality, hobbies, family. (All these information needed to be abslutely random!!)\
        (2) First sample a random personality of MBTI, and then use this one to generate a detailed description of the person's trait.\
        The user id in json is {i} 
        JSON format(just follow the format of this example, also ensure that the generated format is json and there are no problems, use UTF-8 encoding, dont print ```json at the begining):\
        {{
        "User Id": {i},
        "Name": "Lucas Nguyen",
        "Age": 24,
        "Gender": "Male",
        "Major": "Computer Science",
        "Nationality": "Vietnamese",
        "Hobbies": ["Gaming", "Coding", "Playing basketball", "Traveling", "Watching sci-fi movies"],

        "Family Description": "Lucas comes from a family of tech enthusiasts. He has a younger sister, Lily, who is studying design and a supportive father who works as a software engineer. His mother is a former school teacher turned entrepreneur, which has instilled a sense of innovation and creativity in Lucas. Family gatherings often revolve around tech discussions, gaming sessions, and sharing travel experiences, which nurtured Lucas's fascination with both technology and exploration.",

        "MBTI Personality Type": "INTJ (Introverted, Intuitive, Thinking, Judging)",

        "Personality Description": "As an INTJ, Lucas is a strategic thinker and a problem solver. He favors independence and is often found engaging in deep and thoughtful pursuits rather than small talk. His introverted nature allows him to focus intensely on his studies, particularly in complex subjects like algorithms and software development, making him well-suited for his Computer Science major. He thrives when given the freedom to explore his ideas and interests without imposing social pressures.

        Being intuitive, Lucas is not just focused on the here and now—he thinks ahead and looks for patterns. This future-oriented thinking drives him to seek innovative solutions in both his studies and hobbies. He often spends hours coding personal projects or engaging in hackathons, where he loves to collaborate with others to build meaningful applications.

        Lucas's thinking trait means he values logic and objectivity. He tackles problems analytically, preferring data and rational thought over emotions in decision-making. This trait helps him excel academically and provides a structured framework for his projects, resulting in high academic performance.

        As a judging personality type, Lucas appreciates organization and planning. He sets clear goals for himself, making definite plans for his future—whether in his educational trajectory or personal life. This characteristic also manifests in his involvement in gaming, where strategy and foresight are key components of becoming a successful player.

        In summary, Lucas Nguyen is a determined and analytical individual who is dedicated to mastering his field of study while pursuing his passion for technology. His blend of independence and strategic thinking positions him for a successful career in the tech industry, as he aims to create impactful software that can change the world."
        }}"""

        output_1 = model.query(prompt_description)
        # print(output)      

        with open(f"data/description{i}.json", "w", encoding="utf-8") as file:
            file.write(output_1)

        prompt_stages = f"""
        According to {output_1},\
        Following 
        Generate a emotional problem that the student probably face in real life(Can be any possible emotional problem), \
        and you are required provide details (enclude imaginary people and situation related with the event) in the generated case. \
        [requirements] - Divide the event into 4 stages. - In the end of each stages, conclude the mental state of the fake person (his/her emotions, his attitudes towards other people/thing in the event.). 
        Place the mental state in bracket **Mental State** ["state1", "state2", ...] - The first and second stages set the background of the event. 
        Until the last stage, the challenge should be still unsolved. - Associate date with each event. \
        The user id in json is {i} 
        JSON format(just follow the format of this example, also ensure that the generated format is json and there are no problems, use UTF-8 encoding):
        {{
            "User Id": {i},
            "Event": {{
                "Stage 1": {{
                    "Date": "2023-09-15",
                    "Description": "...",
                    "Mental State": ["..", ..., ".."]
                }},
                "Stage 2": {{
                    "Date": "2023-09-30",
                    "Description": "...",
                    "Mental State": ["..", ..., ".."]
                }},
                "Stage 3": {{
                    "Date": "2023-10-20",
                    "Description": "...",
                    "Mental State": ["..", ..., ".."]
                }},
                "Stage 4": {{
                    "Date": "2023-11-05",
                    "Description": "...",
                    "Mental State": ["..", ..., ".."]
                }}
            }}
        }}
        """
        output_2 = model.query(prompt_stages)
        # print(output_2)
        with open(f"data/story{i}.json", "w", encoding="utf-8") as file:
            file.write(output_2)


        prompt_dialogues = f"""
        According to the stages {output_2}, and the profile {output_1}\
        Generate a (20~30)-turn emotional support dialogue between an student ("Student") and an AI consultant ("Counselor"), under the context of each stage. \
        In the dialog, our student seek support from the consultant and discuss on the event he is facing at that stage. \
        The consultant is trying to show empathy, give emotional support and suggestions. \
        Requirements: Include greetings, warmup smalltalks as well as fairwell. Assume in the first dialog the student meet the counselor for the first time, so he will introduce himself.\
        The user id in json is {i} 
        Also use the JSON Format, also ensure that the generated format is json and there are no problems, use UTF-8 encoding, start with {{ }}: 
        {{
        "User Id": {i},
        "Stage 1 dialogue": 
        {{"timestamp": (time),
        "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}, 
        "Stage 2 dialogue": 
        {{"timestamp": (time),
        "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }},
        "Stage 3 dialogue": 
        {{"timestamp": (time),
        "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}, 
        "Stage 4 dialogue": 
        {{"timestamp": (time),
        "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}
        ...
        }}
        
        """

        # {{
        # "User Id": {i},
        # "Stage 1 dialogue": 
        # {{"timestamp": (time),
        # "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}, 
        # "Stage 2 dialogue": 
        # {{"timestamp": (time),
        # "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }},
        # "Stage 3 dialogue": 
        # {{"timestamp": (time),
        # "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}, 
        # "Stage 4 dialogue": 
        # {{"timestamp": (time),
        # "Dialogue": {{Student: xxx, Counselor: xxx, Student: xxx, Counselor: xxx ...}} }}
        # ...
        # }}


        output_3 = model.query(prompt_dialogues)
        # print(output_3)


        with open(f"data/example{i}.json", "w", encoding="utf-8") as file:
            file.write(output_3)


        if i%8 == 0:
            model.reset()