import os

import requests
from fastapi import FastAPI
from pydantic import BaseModel

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://ollama:11434")
QDRANT_URL = os.environ.get("QDRANT_URL", "http://qdrant:6333")

EMBED_MODEL = "nomic-embed-text"
GENERATE_MODEL = "llama3.2:1b"
COLLECTION_NAME = "k8s_docs"
VECTOR_SIZE = 768

DOCS = [
    "A Pod is the smallest deployable unit in Kubernetes.",
    "A Deployment manages a set of replica Pods and handles rolling updates.",
    "A Service provides a stable network endpoint for a set of Pods.",
    "A ConfigMap stores non-sensitive configuration data as key-value pairs.",
    "A PersistentVolumeClaim requests storage for a Pod to use.",
    "A Namespace provides a way to divide cluster resources between multiple users.",
]

app = FastAPI()


class AskRequest(BaseModel):
    question: str


def embed_text(text: str) -> list[float]:
    response = requests.post(
        f"{OLLAMA_URL}/api/embeddings",
        json={"model": EMBED_MODEL, "prompt": text},
    )
    response.raise_for_status()
    return response.json()["embedding"]


def ensure_collection():
    response = requests.get(f"{QDRANT_URL}/collections/{COLLECTION_NAME}")
    if response.status_code == 200:
        return
    requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}",
        json={"vectors": {"size": VECTOR_SIZE, "distance": "Cosine"}},
    ).raise_for_status()


@app.on_event("startup")
def load_docs():
    ensure_collection()
    points = [
        {"id": i, "vector": embed_text(doc), "payload": {"text": doc}}
        for i, doc in enumerate(DOCS)
    ]
    requests.put(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points",
        json={"points": points},
    ).raise_for_status()


@app.post("/ask")
def ask(request: AskRequest):
    question_vector = embed_text(request.question)

    search_response = requests.post(
        f"{QDRANT_URL}/collections/{COLLECTION_NAME}/points/search",
        json={"vector": question_vector, "limit": 3, "with_payload": True},
    )
    search_response.raise_for_status()
    hits = search_response.json()["result"]
    snippets = [hit["payload"]["text"] for hit in hits]

    context = "\n".join(f"- {snippet}" for snippet in snippets)
    prompt = (
        "Answer the question using only the context below.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {request.question}\n"
        "Answer:"
    )

    generate_response = requests.post(
        f"{OLLAMA_URL}/api/generate",
        json={"model": GENERATE_MODEL, "prompt": prompt, "stream": False},
    )
    generate_response.raise_for_status()
    answer = generate_response.json()["response"]

    return {"answer": answer, "retrieved_snippets": snippets}
