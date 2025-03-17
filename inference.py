from dataset import MultiSessionDialog
from lm_backend import OpenAIAgent
from lm_backend import DeepSeekAgent
from memory import get_fact_retrieval_prompt, get_memory_update_prompt
import datetime
import json

def manage_memories(prompt,model):
    response = model.query(prompt,reset=True) 
    return response

def memory_update(old_memories,conversation,model):
    facts = manage_memories(get_fact_retrieval_prompt(conversation),model)
    new_memories  = manage_memories(get_memory_update_prompt(old_memories,facts),model)
    print("finishing updating memory!")
    return new_memories

def write_json(file_path,data):
    with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)

def generate_answer(model, dialogue, question, memory=None):
    """Generates an answer using GPT-4 mini model."""
    if memory:
        prompt = f'You are the emotional counsellor to students. Below is the latest conversation with a student. \n{dialogue}\n and history conversation memory {memory}. \nNow assessing your understanding of the student\'s situation by answering the question: {question}. Just give the answer'
    else:
        prompt = f'You are the emotional counsellor to students. Below is the latest conversation with a student. \n{dialogue}\n. \nNow assessing your understanding of the student\'s situation by answering the question: {question}. Just give the answer'
    
    return model.query(prompt, reset=True)

def process_qa(model, user_id, dialogue, question_wm, question_wom, gold_answer, memory, output_list, filename):
    """Processes QA pairs and writes results into a JSON file."""
    print("start generating!")
    answer_wm = generate_answer(model, dialogue, question_wm, memory)
    answer_wom = generate_answer(model, dialogue, question_wom)
    
    output = {
        'User Id': user_id,
        'question': question_wm,
        'answer_wm': answer_wm,
        'answer_wom': answer_wom,
        'gold_answer': gold_answer
    }
    output_list.append(output)
    write_json(filename, output_list)




if __name__ == '__main__':
    #gpt_4_mini_model = OpenAIAgent()
    ds_model = DeepSeekAgent()
    print("Successful model calling")
    dataset = MultiSessionDialog()
    n = len(dataset)
    data_simple = []
    data_complex = []
    for j in range(1,n+1):
        dialog, qa = dataset[j]
        Id = dialog['User Id']
        simple_question, simple_gold_answer = qa['simple_QA']['question'], qa['simple_QA']['answer']
        complex_question, complex_gold_answer = qa['long_term_QA']['question'], qa['long_term_QA']['answer']
        k = 4 # number of dialogue stage
        memory = {}
        for i in range(1, k+1):
            dialogue_key = f'Stage {i} dialogue'
            stage_dialogue = dialog[dialogue_key]
            memory = memory_update(memory,stage_dialogue,ds_model)
        # Processing Complex QA
        process_qa(ds_model, Id, stage_dialogue, complex_question, complex_question, complex_gold_answer, memory, data_complex, "complex_QA.json")

        # Processing Simple QA
        process_qa(ds_model, Id, stage_dialogue, simple_question, simple_question, simple_gold_answer, memory, data_simple, "simple_QA.json")

        
            
        
        
    



