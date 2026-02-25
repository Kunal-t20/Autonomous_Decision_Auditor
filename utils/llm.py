import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq

load_dotenv()

# ---------- TEST FLAG ----------
TEST_MODE = os.getenv("TEST_MODE", "false").lower() == "true"


def call_llm(prompt: str) -> str:

    # ----- TEST MODE -----
    if TEST_MODE:
        return mock_llm(prompt)

    # ----- REAL LLM -----
    groq_api_key = os.getenv("groq_api_key")

    if not groq_api_key:
        raise ValueError("groq_api_key not found in env")

    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=groq_api_key,
        temperature=0.0
    )

    response = llm.invoke(prompt)


    return response.content


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
