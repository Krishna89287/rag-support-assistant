"""Lightweight automated evaluation for answer quality. Approximates the three
metrics support teams care about: faithfulness, relevancy and hallucination."""


def evaluate(answer: str, context: str, query: str) -> dict:
    ans_words = set(answer.lower().split())
    ctx_words = set(context.lower().split())
    q_words = set(query.lower().split())
    overlap = ans_words & ctx_words
    faithfulness = round(len(overlap) / max(len(ans_words), 1), 2)
    relevancy = round(len(ans_words & q_words) / max(len(q_words), 1), 2)
    hallucination = round(1 - faithfulness, 2)
    return {"faithfulness": faithfulness, "relevancy": relevancy, "hallucination_rate": hallucination}
