# Architecture

```
question -> input guardrails -> retrieve (BM25, with citations)
         -> answer generation (LLM, grounded + cited)
         -> output guardrails (PII redaction)
         -> automated evaluation (faithfulness, relevancy, hallucination)
         -> response + KPIs
```

## Design notes
- Every answer carries citations to the source documents, so reviewers and
  customers can trace the response back to the knowledge base.
- Automated evaluation scores each answer, which lets a team track answer quality
  over time rather than relying on spot checks.
- Guardrails run on input (injection) and output (PII redaction).
- Prometheus exposes query volume, block rate and a resolution proxy as KPIs.
- Runs offline in mock mode; set GROQ_API_KEY for real answers.
