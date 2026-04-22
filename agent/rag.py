import json
import os
import pickle
from typing import List, Dict

import faiss
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv
from google import genai

load_dotenv()

INDEX_PATH = "data/faiss_index.bin"
DOCS_PATH = "data/retrieved_docs.pkl"
EMBED_MODEL_NAME = "all-MiniLM-L6-v2"

_embedder = None


def get_embedder():
    global _embedder
    if _embedder is None:
        _embedder = SentenceTransformer(EMBED_MODEL_NAME)
    return _embedder


def get_genai_client():
    api_key = os.getenv("GOOGLE_API_KEY")
    if not api_key:
        raise ValueError("GOOGLE_API_KEY not found in environment/secrets")
    return genai.Client(api_key=api_key)


def load_knowledge_base() -> Dict:
    with open("data/knowledge_base.json", "r", encoding="utf-8") as file:
        return json.load(file)


def build_documents() -> List[str]:
    kb = load_knowledge_base()
    docs = []

    plans = kb.get("plans", [])
    for plan in plans:
        plan_name = plan.get("name", "")
        price = plan.get("price", "")
        videos = plan.get("videos_per_month", "")
        resolution = plan.get("resolution", "")
        features = ", ".join(plan.get("features", [])) if plan.get("features") else "No extra features"

        docs.append(
            f"{plan_name}. Price: {price}. Usage: {videos}. "
            f"Resolution: {resolution}. Features: {features}."
        )

    policies = kb.get("policies", [])
    for policy in policies:
        docs.append(f"Company policy: {policy}.")

    return docs


def build_vector_store():
    docs = build_documents()
    embedder = get_embedder()
    embeddings = embedder.encode(docs, convert_to_numpy=True).astype("float32")

    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)

    with open(DOCS_PATH, "wb") as file:
        pickle.dump(docs, file)


def ensure_vector_store():
    if not os.path.exists(INDEX_PATH) or not os.path.exists(DOCS_PATH):
        build_vector_store()
        return

    expected_docs = build_documents()
    try:
        with open(DOCS_PATH, "rb") as file:
            cached_docs = pickle.load(file)
        if cached_docs != expected_docs:
            build_vector_store()
    except Exception:
        build_vector_store()


def retrieve_context(user_message: str, top_k: int = 2) -> List[str]:
    ensure_vector_store()

    embedder = get_embedder()
    query_embedding = embedder.encode([user_message], convert_to_numpy=True).astype("float32")
    index = faiss.read_index(INDEX_PATH)

    with open(DOCS_PATH, "rb") as file:
        docs = pickle.load(file)

    _, indices = index.search(query_embedding, top_k)

    retrieved_docs = []
    for idx in indices[0]:
        if 0 <= idx < len(docs):
            retrieved_docs.append(docs[idx])

    return retrieved_docs


def fallback_answer(user_message: str, context_docs: List[str]) -> str:
    text = user_message.lower()

    if "price" in text or "pricing" in text:
        return (
            "AutoStream has two plans:\n"
            "- Basic Plan: $29/month\n"
            "- Pro Plan: $79/month"
        )

    if "feature" in text or "features" in text:
        return (
            "Basic Plan has no extra features. "
            "Pro Plan includes AI captions and 24/7 support."
        )

    if "refund" in text:
        return "No refunds are available after 7 days."

    if "support" in text:
        return "24/7 support is available only on the Pro plan."

    if "basic" in text and "pro" in text:
        return (
            "Basic Plan costs $29/month with 10 videos/month and 720p resolution. "
            "Pro Plan costs $79/month with unlimited videos, 4K resolution, AI captions, and 24/7 support."
        )

    if "basic plan" in text:
        return "Basic Plan costs $29/month, includes 10 videos/month, and supports 720p resolution."

    if "pro plan" in text:
        return "Pro Plan costs $79/month, includes unlimited videos, 4K resolution, AI captions, and 24/7 support."

    if context_docs:
        return "Here’s what I found:\n" + "\n".join(f"- {doc}" for doc in context_docs)

    return "Sorry, that detail is not available in the current knowledge base."


def generate_answer_from_context(user_message: str, context_docs: List[str]) -> str:
    if not context_docs:
        return "Sorry, that detail is not available in the current knowledge base."

    context = "\n".join(context_docs)

    prompt = f"""
You are an AI sales assistant for AutoStream.

Answer the user's question using ONLY the context below.
If the answer is not present in the context, reply exactly:
Sorry, that detail is not available in the current knowledge base.

Context:
{context}

User Question:
{user_message}

Give a short, clear, professional answer.
"""

    try:
        client = get_genai_client()
        response = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=prompt
        )

        if hasattr(response, "text") and response.text:
            return response.text.strip()

    except Exception:
        pass

    return fallback_answer(user_message, context_docs)


def retrieve_answer(user_message: str) -> str:
    context_docs = retrieve_context(user_message, top_k=2)
    return generate_answer_from_context(user_message, context_docs)
