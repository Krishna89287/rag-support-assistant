from prometheus_client import Counter, Histogram
QUERIES = Counter("support_queries_total", "Support queries answered")
BLOCKED = Counter("support_blocked_total", "Queries blocked by guardrails")
RESOLVED = Counter("support_resolved_total", "Answers with confident grounding")
LATENCY = Histogram("support_query_seconds", "Query latency")
