import time
from fastapi import FastAPI
from fastapi.responses import Response
from pydantic import BaseModel
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from app.knowledge import retrieve
from app.llm import llm
from app.guardrails import check_input, redact
from app.evaluation import evaluate
from app.metrics import QUERIES, BLOCKED, RESOLVED, LATENCY
from app.config import settings

app = FastAPI(title="Enterprise RAG Support Assistant", version="1.0.0",
              description="Answers customer questions from a knowledge base with citations, guardrails and automated evaluation.")


class Query(BaseModel):
    question: str


@app.get("/health")
def health():
    return {"status": "ok", "llm_mode": llm.mode}


@app.post("/ask")
def ask(req: Query):
    start = time.time()
    QUERIES.inc()
    if settings.enable_guardrails:
        gate = check_input(req.question)
        if gate["blocked"]:
            BLOCKED.inc()
            return {"answer": "Your request was blocked by input guardrails.", "blocked": True, "reason": gate["reason"]}

    docs = retrieve(req.question)
    context = "\n".join(f"[{d['id']}] {d['text']}" for d in docs)
    prompt = ("Answer the customer question using only the context. Cite the source ids in brackets. "
              "If the context does not answer it, say so.\n"
              f"Context:\n{context}\n\nQuestion: {req.question}")
    answer = redact(llm.complete(prompt)) if settings.enable_guardrails else llm.complete(prompt)
    scores = evaluate(answer, context, req.question)
    if scores["faithfulness"] >= 0.3:
        RESOLVED.inc()
    LATENCY.observe(time.time() - start)
    return {
        "answer": answer,
        "citations": [d["id"] for d in docs],
        "evaluation": scores,
        "blocked": False,
    }


@app.get("/metrics")
def metrics():
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)
