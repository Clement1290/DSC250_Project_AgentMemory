from evaluator import Evaluator
import json

def data_load(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def batch_evaluate(data,evaluator):
    gold_answer = []
    wm_answer = []
    wom_answer = []
    for info in data:
        gold_answer.append(info["gold_answer"])
        wm_answer.append(info["answer_wm"])
        wom_answer.append(info["answer_wom"])
    wm_result = evaluator.compute_all_score(gold_answer, wm_answer)
    wom_result = evaluator.compute_all_score(gold_answer, wom_answer)
    return wm_result, wom_result
        
    
if __name__ == "__main__":
    evaluator = Evaluator()
    simple_data = data_load("../result/simple_QA.json")
    complex_data = data_load("../result/complex_QA.json")
    simple_wm_result, simple_wom_result = batch_evaluate(simple_data,evaluator)
    complex_wm_result, complex_wom_result = batch_evaluate(complex_data,evaluator)
    output = {"simple_wm_result":simple_wm_result,
              "simple_wom_result":simple_wom_result,
              "complex_wm_result":complex_wm_result,
              "complex_wom_result":complex_wom_result}
    print(output)
    with open("output.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
