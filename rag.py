import faiss
import numpy as np
from openai import OpenAI

EMBED_MODEL = "text-embedding-ada-002"
EMBED_DIM = 1536
API_KEY = "YOUR_API_KEY"

# Initialize OpenAI client
client = OpenAI(api_key= API_KEY)

# Global dictionary to store user-specific FAISS indices
user_indexes = {}

def get_user_index(user_id: str):
    """
    Returns (or creates) a FAISS index & stored_facts list for the given user_id.
    """
    if user_id not in user_indexes:
        user_indexes[user_id] = {
            "index": faiss.IndexFlatL2(EMBED_DIM),
            "stored_facts": []  # List of tuples: (fact_text, fact_id, timestamp)
        }
    return user_indexes[user_id]

def embed_text(text: str) -> np.ndarray:
    """
    Calls OpenAI to embed text and returns a numpy array.
    """
    response = client.embeddings.create(
        model=EMBED_MODEL,
        input=[text]  
    )
    emb = response.data[0].embedding
    return np.array(emb, dtype=np.float32)

def add_fact(user_id: str, fact_text: str, fact_id: str, timestamp: float):
    """
    Adds a fact to the FAISS index with a timestamp.
    """
    user_data = get_user_index(user_id)
    vec = embed_text(fact_text).reshape(1, -1)
    user_data["index"].add(vec)
    user_data["stored_facts"].append((fact_text, fact_id, timestamp))

def retrieve_long_term_facts(user_id: str):
    """
    Retrieves all stored facts, prioritizing the most recent session.
    """
    user_data = get_user_index(user_id)
    if user_data["index"].ntotal == 0:
        return {}

    indexed_facts = sorted(user_data["stored_facts"], key=lambda x: x[2], reverse=True)
    categorized_facts = {"Recent Session": [], "Long-Term": []}
    seen_facts = set()

    # Assign most recent session fact
    if indexed_facts:
        recent_fact = indexed_facts[0][0]
        if recent_fact not in seen_facts:
            categorized_facts["Recent Session"].append(recent_fact)
            seen_facts.add(recent_fact)

    # Assign remaining facts to long-term storage
    for fact_text, fact_id, timestamp in indexed_facts[1:]:
        if fact_text not in seen_facts:
            categorized_facts["Long-Term"].append(fact_text)
            seen_facts.add(fact_text)

    return categorized_facts