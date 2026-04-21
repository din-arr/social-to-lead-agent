# 🤖 AutoStream AI Agent

Conversational AI system for product queries, lead qualification, and lead capture.

---

## 🚀 Features

- RAG-based question answering (FAISS + embeddings)
- Intent classification (greeting, inquiry, lead intent)
- Multi-step lead capture (name → email → platform)
- Streamlit chat UI
- Fallback system for reliability (handles API failures)

---

## 🧠 Tech Stack

- Python
- Streamlit
- FAISS (vector search)
- Sentence Transformers
- Gemini API (LLM)
- RAG (Retrieval-Augmented Generation)

---

## 💡 How it works

1. User asks a question  
2. Intent is detected  
3. If product query → RAG retrieves answer  
4. If user shows interest → lead flow starts  
5. System collects:
   - Name
   - Email
   - Platform  
6. Lead is captured via tool

---

## 🛠️ Run Locally

```bash
pip install -r requirements.txt
streamlit run app.py
