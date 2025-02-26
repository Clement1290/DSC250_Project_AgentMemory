from lm_backend import OpenAIAgent
import json
from dataset import MultiSessionDialog

def GPT4_evaluation(question, answer1,answer2,model,dialogue):
    comparing_prompt = f"Q:{question}\n A1{answer1}\n A2{answer2}\nYou are a helpful, harmless, and precise assistant who checks the quality of the answer of the question above based on the emotional dialogue between \
    a student and counselor below. We would like to ask for your feedback on which answer is better? Just return A1 or A2.\n {dialogue}"
    rating_prompt = f"Q:{question}\n A1{answer1}\n A2{answer2}\nYou are a helpful, harmless, and precise assistant who checks the quality of the answer of the question above based on the emotional dialogue between \
    a student and counselor below. We would like to ask for your feedback on the quality of the answer on the scale of 10 (1 represents bad, 10 represents very good)? \
    Output in the following format: \"{{\"A1\": \[an integer number between 1 and 10\], \"A2\": \[an integer numberbetween 1 and 10\]}}\".\n {dialogue}"
    comparing_result = model.query(comparing_prompt,reset=True)
    rating = model.query(rating_prompt,reset=True)
    return {"comparing_result":comparing_result,"rating_result":json.loads(rating)}
    
def data_load(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def evaluate_data(data, dataset, model):
    compare_dic = {"A1": 0, "A2": 0}
    rating_dict = {"A1": 0, "A2": 0}
    n = len(data)

    for i in range(n): 
        question = data[i]["question"]
        answer_wm = data[i]["answer_wm"]
        answer_wom = data[i]["answer_wom"]
        dialog, _ = dataset[i+1]

        result = GPT4_evaluation(question, answer_wm, answer_wom, model, dialog)
        
        # 记录比较结果
        if result["comparing_result"] == "A1":
            compare_dic["A1"] += 1
        else:
            compare_dic["A2"] += 1
        
        # 记录评分
        rating_dict["A1"] += int(result["rating_result"]["A1"])/n
        rating_dict["A2"] += int(result["rating_result"]["A2"])/n

    return compare_dic, rating_dict  # 返回计算结果

if __name__ == "__main__":
    simple_data = data_load("result/simple_QA.json")
    complex_data = data_load("result/complex_QA.json")
    dataset = MultiSessionDialog()
    n = len(dataset)
    model = OpenAIAgent()
    simple_compare, simple_rating = evaluate_data(simple_data, dataset, model)
    complex_compare, complex_rating = evaluate_data(complex_data, dataset, model)
    
    with open("output_simple_rating.json", "w", encoding="utf-8") as f:
        json.dump(simple_rating, f, ensure_ascii=False, indent=4)
    with open("output_complex_rating.json", "w", encoding="utf-8") as f:
        json.dump(complex_rating, f, ensure_ascii=False, indent=4)
    with open("output_simple_compare.json", "w", encoding="utf-8") as f:
        json.dump(simple_compare, f, ensure_ascii=False, indent=4)
    with open("output_complex_compare.json", "w", encoding="utf-8") as f:
        json.dump(complex_compare, f, ensure_ascii=False, indent=4)
    
        
    
        