from torch.utils.data import Dataset
from datasets import load_dataset


class AUGESC(Dataset):
    def __init__(self, cache_dir="../cache/dataset"):
        raw_dataset = load_dataset("thu-coai/augesc", cache_dir=cache_dir)
        raw_dataset = raw_dataset["train"]
        self.data = []
        for entry in raw_dataset:
            self.data.append(eval(entry["text"]))
    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, idx):
        return self.data[idx]


if __name__ == "__main__":
    dataset = AUGESC()
    print(f"[Dataset] {len(dataset)=}")
    print("example")
    for chat in dataset[0]:
        print(f"{chat[0]}: {chat[1]}")
