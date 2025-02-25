import sys
import json

sys.path.append("..")
from lm_backend import OpenAIAgent
from tqdm import tqdm
from random import sample


PROMPT_SIMPLE = """Generated dialog
{dialog}

Given 4 session dialogs, you are supposed to came up with one question related to the final dialog.
[requirements]
- {specification}
- The answer should be possible to retrieve in the original dialog (so that it is part of the evidence).
- The answer length should be minimal, containing one precise information.
[format]:
{{
    "evidence":  {{"stage": 4, "role": "Student/Counselor", "quote": "..."}},
    # In the question, use the student's name. 
    "question": "...",
    "answer: "...",
}}
"""

SPECIFICATIONS = [
    "The question should be related to the student's mental condition (for example, what caused it, how to solve it, how it relates with other things, and so on)",
    "The question should focus on a detail related to the student.(But possibly ask in all aspects, for example what is something that has xxx attribute)",
    "The question should be related to what the student plan to do next after the dialog.",
    "The question should be related to what the student just did before the dialog."
]

def get_simple_qa(agent, dialogs):
    while True:
        prompt = PROMPT_SIMPLE.format(dialog=dialogs, specification=sample(SPECIFICATIONS, 1) )
        qa_simple = agent.query(prompt,reset=True)
        try:
            qa_simple = json.loads(qa_simple)
            break
        except:
            print("Invalid QA format, try again")
    print(qa_simple)
    return qa_simple

OBSERVE_PROMPT = """{event}

From the event, identify a change from the student.

[requirement]
- organize the result in the following format
{{
    "aspect": "..."(In a complete sentence),
    "previous": {{"stage": 1/2/3/4, "description": "..."}},
    "reason":{{"stage": 1/2/3/4, "description": "..."}},
    "after": {{"stage": 1/2/3/4, "description": "..."}}
}}
"""

LONG_TERM_PROMPT = """In the following conversation:
{dialog}

Identify the following observation:
observation = {observation}

Construct a question based on the observation that needs to be answered by both `observation["previous"]` and `observation["reason"]`

[requirement]
- The question ask about the **previous** condition and the **reason*, an example is "before observation["after"] how is XXX(the student's name) like, and what prompts XXX(the student's name) to change?" (However in a more natural and informative way in the actual generated question.)
- Do not mention stage1/2/3/4 in the question, as this is only a denotation for analysis.
- organize the result in the following format (do not add markdown code bracket):

{{
    "question": "..."(be precise),
    "local evidence": {{"stage": 1/2/3/4, "role": "Student/Counselor", "quote": "..."}},
    #(an evidence in the dialog that support `observation["after"]`, found in the observation["after"]["stage"]),
    "long-term evidence":  {{"stage": 1/2/3/4, "role": "Student/Counselor", "quote": "..."}},
    #(an evidence in the dialog that support observation["previous"], found in the observation["previous"]["stage"]),
    "insight evidence":  {{"stage": 1/2/3/4, "role": "Student/Counselor", "quote": "..."}},
    #(an evidence in the dialog that support observation["reason"], found in the observation["reason"]["stage"]),
    "answer: "..."
    #(The answer should user as much words from quote as possible, and the answer should be concise and precise)
}}
"""

def get_long_term_qa(agent, dialogs, events):
    prompt = OBSERVE_PROMPT.format(event=events)
    observation = agent.query(prompt,reset=True)
    while True:
        prompt = LONG_TERM_PROMPT.format(dialog=dialogs, observation=observation)
        long_term_qa = agent.query(prompt,reset=True)
        try:
            long_term_qa = json.loads(long_term_qa)
            break
        except:
            print("Invalid QA format, try again")
    print(long_term_qa)
    return long_term_qa


if __name__ == "__main__":
    agent = OpenAIAgent()
    for i in tqdm(range(1, 101)):
        with open(f"data/description{i}.json", encoding="utf-8") as f:
            profile = f.read()
        with open(f"data/story{i}.json", encoding="utf-8") as f:
            events = f.read()
        with open(f"data/example{i}.json", encoding="utf-8") as f:
            dialogs = f.read()        
        simple_qa = get_simple_qa(agent, dialogs)
        agent.reset()
        long_term_qa = get_long_term_qa(agent, dialogs, events)
        agent.reset()
        out = {
            "User Id": i,
            "simple_QA": simple_qa,
            "long_term_QA": long_term_qa,
        }
        with open(f"data/QA_{i}.json", mode="w", encoding="utf-8") as f:
            json.dump(out, f, indent=4)




