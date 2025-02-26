import os
import json
#from torch.utils.data import Dataset
from glob import glob

BASE_PATH = os.path.dirname(os.path.abspath(__file__))

# MBTI = ["INFJ", "INFP", "INTJ", "INTP", "ENTJ", "ENTP", "ENFJ", "ENFP", "ISTJ", "ISTP", "ISFJ", "ISFP", "ESTP", "ESTJ", "ESFP", "ESFJ"]

# def get_persona_prompt():
#     mbti = sample(MBTI, 1)
#     prompt = f"""Please generate a fake profile of a college student (undergraduate/graduate student) with  descriptions. 
#     [requirements] 
#     (1) Include basic information about the person, such as name, age, gender, nationality.
#     (2) Generate the student's acedemia life (major, which year of study, possible school activities)
#     (3) Generate the student's personal life (hobbies, interests, activities, etc.), however this section should be of minimal length.
#     (4) Generate the student's family life, also minimal length.
#     (3) Enforce the student's personality as {mbti}, and then use this one to generate a detailed description of the person's trait, 
#     explain their motivations, strengths, challenges. (also include the MBTI type in the profile) 
#     However this section should be precise and should not contain any suggestion of the student's actual experience.
#     """
#     return prompt


class MultiSessionDialog():
    def __init__(self):
        self.N = len(glob(f"{BASE_PATH}\\data\\QA_*.json"))
        self.dialog_files = [f"{BASE_PATH}\\fixed_dialog\\example{i}.json" for i in range(self.N)]
        self.qa_files = [f"{BASE_PATH}\\data\\QA_{i}.json" for i in range(self.N)]
        
    def __len__(self):
        return self.N
    
    def __getitem__(self, idx):
        with open(self.dialog_files[idx]) as f:
            dialog = json.load(f)
        with open(self.qa_files[idx]) as f:
            qa = json.load(f)
        return dialog, qa



if __name__ == "__main__":
    ds = MultiSessionDialog()
    print(ds[3])
