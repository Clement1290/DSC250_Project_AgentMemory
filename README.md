# AI-Driven Mental Health Support with Long-Term Memory




## File structure

`auto_evaluation`: Auto evaluation
usage:
```python
from auto_evaluation import Evaluator

references= ["The cat is on the mat.","I love u"]
generated_texts = ["The cat is on the dog.","I like u"]
evaluator = Evaluator()
results = evaluator.compute_all_score(references, generated_texts)
```


`./dataset`: Load dataset
usage:
```python
from dataset import AUGESC

dataset = AUGESC()
```


`./lm_backend`: Language model backend (openai/ollama)
usage:
```python
from lm_backend import OpenAIAgent

model = OpenAIAgent()

prompt = "What is the capital of France?"
agent.query(prompt)
```


## 使用多轮对话数据集
在根目录下，运行
```python
from dataset import MultiSessionDialog

dataset = MultiSessionDialog()
print(len(dataset))

dialog, qa = dataset[0]
print(dialog)
print(qa)
```