# %%
from augesc import AUGESC

def get_dataset(dataset_name, **kwargs):
    if dataset_name == "augesc":
        return AUGESC(**kwargs)
    else:
        raise NotImplementedError