"""Knowledge base with BM25 retrieval and citations. Replace the in-memory docs
with your own product or support content, or wire to a vector store."""
from rank_bm25 import BM25Okapi

DOCS = [
    {"id": "KB-1", "text": "To reset your password, open Settings, choose Security, then Reset Password. A reset link is emailed and is valid for 30 minutes."},
    {"id": "KB-2", "text": "Refunds are processed within 5 to 7 business days to the original payment method. Contact support if it has not arrived after 7 days."},
    {"id": "KB-3", "text": "The free plan includes 3 projects and 1 GB storage. Paid plans add unlimited projects, priority support and SSO."},
    {"id": "KB-4", "text": "To enable two factor authentication, go to Security and scan the QR code with an authenticator app, then enter the 6 digit code."},
    {"id": "KB-5", "text": "API rate limits are 100 requests per minute on the free plan and 1000 on paid plans. Exceeding the limit returns HTTP 429."},
]
_tok = [d["text"].lower().split() for d in DOCS]
_bm25 = BM25Okapi(_tok)


def retrieve(query: str, k: int = 3):
    scores = _bm25.get_scores(query.lower().split())
    ranked = sorted(range(len(DOCS)), key=lambda i: scores[i], reverse=True)
    return [DOCS[i] for i in ranked[:k] if scores[i] > 0] or [DOCS[ranked[0]]]
