
import sys
import json

sys.path.append("..")
from lm_backend import OpenAIAgent, OllamaAgent
from tqdm import tqdm


PROMPT = """
Fix the following text into strict json format:

{text}

[Instruction]:
- For dialog section, reformulate it as
"Dialogue": {{
    [
        {{"role": "Student", "round":1, "content": "xxx"}},
        {{"role": "Counselor", "round":1, "content": "xxx"}},
        {{"role": "Student", "round":2, "content": "xxx"}},
        ...
    ]
}}
- Eliminate all non-ascii characters in the text to the corresponding ascii characters.
- Do NOT use markdown code bracket.
example: `’` -> `'` 
"""

if __name__ == "__main__":
    agent = OpenAIAgent()
    for i in tqdm(range(1, 101)):
        with open(f"data/example{i}.json", "r", encoding="utf-8") as f:
            text = f.read()
        while True:
            prompt = PROMPT.format(text=text)
            fixed = agent.query(prompt,reset=True)
            try:
                fixed = json.loads(fixed)
                break
            except:
                print("Invalid QA format, try again")
        print(fixed)
        with open(f"fixed_dialog/example{i}.json", "w", encoding="utf-8") as f:
            json.dump(fixed, f, indent=4)



