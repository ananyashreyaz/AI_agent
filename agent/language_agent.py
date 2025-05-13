# language_agent.py

from fastapi import FastAPI
from pydantic import BaseModel
from langchain.chat_models import ChatOpenAI
from langchain.schema import SystemMessage, HumanMessage
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings
from langchain.chains import RetrievalQA
import pickle
import faiss

app = FastAPI()

# LLM setup
llm = ChatOpenAI(temperature=0, model="gpt-3.5-turbo", openai_api_key="your-api-key")

# Load retriever
def load_retriever():
    with open("metadata.pkl", "rb") as f:
        documents = pickle.load(f)
    index = faiss.read_index("faiss_index.bin")
    embedding_model = OpenAIEmbeddings(openai_api_key="your-api-key")
    vectordb = FAISS(embedding_model.embed_query, index, documents)
    retriever = vectordb.as_retriever(search_kwargs={"k": 3})
    return retriever

retriever = load_retriever()

# LangChain QA chain
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

class LanguageQuery(BaseModel):
    query: str

@app.post("/generate_narrative")
def generate_narrative(request: LanguageQuery):
    result = qa_chain({"query": request.query})
    return {
        "answer": result["result"],
        "sources": [doc.metadata for doc in result["source_documents"]]
    }
