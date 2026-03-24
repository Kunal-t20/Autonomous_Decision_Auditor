import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

from services.redis_cache import llm_cache_get, llm_cache_key, llm_cache_set

load_dotenv()

# ---------- TEST FLAG ----------
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"

LLM_MODEL = "openai/gpt-oss-20b"
LLM_TEMPERATURE = 0.0


def call_llm(prompt: str) -> str:
    if TEST_MODE:
        return mock_llm(prompt)

    groq_api_key = os.getenv("groq_api_key")
    if not groq_api_key:
        raise ValueError("groq_api_key not found in env")

    cache_key = llm_cache_key(LLM_MODEL, LLM_TEMPERATURE, prompt)
    cached = llm_cache_get(cache_key)
    if cached is not None:
        return cached

    llm = ChatGroq(
        model=LLM_MODEL,
        groq_api_key=groq_api_key,
        temperature=LLM_TEMPERATURE,
    )
    response = llm.invoke(prompt)
    content = response.content
    llm_cache_set(cache_key, content)
    return content


def mock_llm(prompt: str) -> str:

    p = prompt.lower()

    if "claim" in p:
        return """
        - AI automates tasks.
        - AI improves efficiency.
        - AI reduces manual errors.
        """

    if "evidence" in p:
        return """
        - Automation software reports
        - Productivity analytics
        - Case studies
        """

    if "counterfactual" in p:
        return "If AI data quality is poor, decision outcome may change."

    if "confidence" in p:
        return "Confidence Score: 0.65"

    return "Default mock response."
