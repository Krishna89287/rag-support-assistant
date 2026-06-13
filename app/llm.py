import os
from app.config import settings


class LLM:
    def __init__(self):
        self._client = None
        self.mode = "mock"
        if settings.llm_ready:
            os.environ["GROQ_API_KEY"] = settings.groq_api_key
            from langchain_groq import ChatGroq
            self._client = ChatGroq(model=settings.groq_model, temperature=0.1)
            self.mode = "groq"

    def complete(self, prompt: str) -> str:
        if self._client is None:
            return "MOCK ANSWER grounded in the retrieved context."
        return self._client.invoke(prompt).content


llm = LLM()
