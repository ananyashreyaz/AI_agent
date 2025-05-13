# agents/retriever_agent.py
from fastapi import FastAPI
from pydantic import BaseModel
import pandas as pd
from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import glob
import os

app = FastAPI()

class QueryRequest(BaseModel):
    query: str

def load_data(data_dir="C:/Users/anany/OneDrive/Desktop/Ananya/Raga_Ai_Agent/data"):
    texts = []
    os.makedirs(data_dir, exist_ok=True)
    for csv_file in glob.glob(f"{data_dir}/*.csv"):
        try:
            df = pd.read_csv(csv_file)
            file_type = csv_file.split('_')[-2]  # e.g., stock, earnings
            for _, row in df.iterrows():
                ticker = row.get('ticker', row.get('Ticker', 'Unknown'))
                text = f"{file_type} for {ticker}: "
                text += ", ".join([f"{k}: {v}" for k, v in row.items() if k.lower() not in ['ticker']])
                texts.append(text)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    return texts

def create_vector_store(texts):
    if not texts:
        return None, None, []
    model = SentenceTransformer('all-MiniLM-L6-v2')
    embeddings = model.encode(texts, show_progress_bar=False)
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings.astype(np.float32))
    return index, model, texts

texts = load_data()
index, model, texts = create_vector_store(texts)

@app.post("/retrieve")
def retrieve(request: QueryRequest):
    if not index or not texts:
        return {"error": "No data indexed"}
    query = request.query
    query_embedding = model.encode([query], show_progress_bar=False)
    distances, indices = index.search(query_embedding.astype(np.float32), k=5)
    results = [texts[idx] for idx in indices[0]]
    return {"query": query, "results": results}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)