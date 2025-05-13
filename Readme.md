
# 📊 RagaAI: Voice-Powered Financial Assistant

RagaAI is a modular, multi-agent system that uses voice commands to provide intelligent financial insights using real-time data, LLM-based analysis, and document retrieval.

---

## 🧠 Architecture Overview

- **🎤 Voice Agent**: Converts voice to text using Whisper, and synthesizes responses via TTS.
- **🧭 Orchestrator**: Routes voice/text queries to appropriate agents and combines results.
- **📈 API Agent**: Fetches stock and market data using Yahoo Finance.
- **📰 Scraping Agent**: Retrieves earnings, news, and filings from FMP.
- **🔍 Retriever Agent**: Uses FAISS & Sentence Transformers to fetch relevant document chunks.
- **📊 Analysis Agent**: Uses LangChain + LLM to perform earnings or risk analysis.
- **🌐 Streamlit App**: Frontend for interacting with the system via voice.

---

## 📦 Libraries Used

### ✅ 1. Orchestrator

```
fastapi
pydantic
requests
re
```

---

### ✅ 2. API Agent (Yahoo Finance)

```
fastapi
pydantic
yfinance
```

---

### ✅ 3. Scraping Agent (Financial Modeling Prep)

```
fastapi
pydantic
requests
```

---

### ✅ 4. Retriever Agent (FAISS + LangChain)

```
fastapi
pydantic
faiss-cpu
sentence-transformers
langchain
tqdm
```


### 5. Analysis Agent (LLM via LangChain)

```
fastapi
pydantic
langchain
openai  # or any LangChain-supported LLM backend
```

---

### 6. Voice Agent (STT + TTS)

```
fastapi
whisper
gTTS
pydub
```



---

### 7. Streamlit App (Frontend)

```
streamlit
requests
soundfile
```

---

## 🔧 Combined Requirements (`requirements.txt`)

```
# Core
fastapi
pydantic
requests
re

# API Agent
yfinance

# Retriever Agent
faiss-cpu
sentence-transformers
langchain
tqdm
# pinecone-client  # Uncomment if Pinecone is used

# Analysis Agent
openai

# Voice Agent
whisper
gTTS
pydub

# Frontend
streamlit
soundfile
```

---

## ⚙️ System Setup

Install FFmpeg (for audio processing):
```bash
sudo apt-get install ffmpeg      # Debian/Ubuntu
brew install ffmpeg              # macOS
```

---

## 🚀 Run the System

Each agent is run as a separate FastAPI service (recommended using different ports):

```bash
uvicorn orchestrator:app --port 8000
uvicorn api_agent:app --port 8001
uvicorn retriever_agent:app --port 8002
uvicorn scraping_agent:app --port 8003
uvicorn analysis_agent:app --port 8004
uvicorn voice_agent:app --port 8005
streamlit run app.py            # Streamlit frontend
```

---

## 📞 Voice Query Workflow

1. 🎤 Speak into Streamlit UI.
2. 🧠 Voice Agent transcribes it to text.
3. 🔗 Orchestrator routes it to appropriate agents.
4. 📚 Retriever fetches relevant documents.
5. 📊 Analyst generates insights.
6. 🔊 Voice Agent speaks final response.

---


