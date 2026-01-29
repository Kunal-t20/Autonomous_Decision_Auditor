import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq


load_dotenv()

def call_llm(prompt: str) -> str:
    groq_api_key = os.getenv("groq_api_key")

    if not groq_api_key:
        raise ValueError("groq_api_key not found in env")


    llm = ChatGroq(
        model="openai/gpt-oss-20b",
        groq_api_key=groq_api_key,
        temperature=0.0
        )
    
    response=llm.invoke(prompt)
    return response


