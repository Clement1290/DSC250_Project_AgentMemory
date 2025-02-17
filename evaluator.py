from rouge.rouge import Rouge
import sys
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

class Evaluator:
    def __init__(self):
        self.rouge = Rouge()
        
    def compute_rouge(self, source, target):
        """Compute rouge-1、rouge-2、rouge-l
        """
        try:
            scores = self.rouge.get_scores(hyps=source, refs=target)
            return {
                'rouge-1': scores[0]['rouge-1']['f'],
                'rouge-2': scores[0]['rouge-2']['f'],
                'rouge-l': scores[0]['rouge-l']['f'],
            }
        except ValueError:
            return {
                'rouge-1': 0.0,
                'rouge-2': 0.0,
                'rouge-l': 0.0,
            }
    
    def compute_rouges_directly(self, references, generated_texts):
        scores = {
            'rouge-1': 0.0,
            'rouge-2': 0.0,
            'rouge-l': 0.0,
        }
        for id, reference in enumerate(references):
            generated = generated_texts[id]
            score = self.compute_rouge(reference, generated)
            for k, v in scores.items():
                scores[k] = v + score[k]
        result = {k: v / len(generated_texts) for k, v in scores.items()}
        return result
    
    def compute_bleu_directly(self, references, generated_texts):
        score = 0.0
        for id, reference in enumerate(references):
            generated = generated_texts[id]
            
            score += sentence_bleu(references=[reference.split()], hypothesis=generated.split(),
                                   smoothing_function=SmoothingFunction().method1)

        score /= len(references)
        return score

    def compute_all_score(self, references, generated_texts):
        rouge_result = self.compute_rouges_directly(references, generated_texts)
        bleu_score = self.compute_bleu_directly(references, generated_texts)
        result_dic = {"rouge-1":rouge_result["rouge-1"], "rouge-2":rouge_result["rouge-2"], "rouge-l":rouge_result["rouge-l"],"BLUE" :bleu_score}
        return result_dic


if __name__ == "__main__":
    references= ["The cat is on the mat.","I love u"]
    generated_texts = ["The cat is on the dog.","I like u"]
    evaluator = Evaluator()
    results = evaluator.compute_all_score(references, generated_texts)
    print(results)








