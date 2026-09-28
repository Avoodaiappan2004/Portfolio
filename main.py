import os
import json

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from groq import Groq

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise Exception("GROQ_API_KEY not found!")


# --------------------------------
# FastAPI
# --------------------------------

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# --------------------------------
# Groq
# --------------------------------

client = Groq(api_key=api_key)


# --------------------------------
# Load portfolio knowledge
# --------------------------------

with open("portfolio_knowledge.json", "r", encoding="utf-8") as file:
    portfolio = json.load(file)


portfolio_content = portfolio["content"]


# --------------------------------
# Split portfolio
# --------------------------------

sections = [
    section.strip()
    for section in portfolio_content.split("\n\n")
    if section.strip()
]


# --------------------------------
# TF-IDF
# --------------------------------

vectorizer = TfidfVectorizer()

section_vectors = vectorizer.fit_transform(sections)


# --------------------------------
# Request format
# --------------------------------

class Question(BaseModel):
    question: str


# --------------------------------
# Home API
# --------------------------------

@app.get("/")
def home():

    return {
        "message": "Portfolio AI API is running"
    }


# --------------------------------
# Chat API
# --------------------------------

@app.post("/chat")
def chat(data: Question):

    question = data.question

    # Convert question into vector
    question_vector = vectorizer.transform([question])

    # Calculate similarity
    similarities = cosine_similarity(
        question_vector,
        section_vectors
    )[0]

    # Get top 5 relevant sections
    top_results = similarities.argsort()[-5:][::-1]

    relevant_sections = []

    for index in top_results:

        if similarities[index] > 0:
            relevant_sections.append(sections[index])

    # Create context
    context = "\n\n".join(relevant_sections)

    # Prompt
    prompt = f"""
You are an AI assistant for Avoodaiappan's portfolio.

Answer the user's question ONLY using the portfolio
context provided below.

Do not invent information.

If the answer is not available in the portfolio, say:

"I couldn't find that information in the portfolio."

PORTFOLIO CONTEXT:

{context}

USER QUESTION:

{question}
"""

    # Groq
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0
    )

    answer = response.choices[0].message.content

    return {
        "question": question,
        "answer": answer
    }