import os
import json

from dotenv import load_dotenv
from groq import Groq

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


# --------------------------------
# Load environment variables
# --------------------------------

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Groq API key not found!")
    exit()


# --------------------------------
# Create Groq client
# --------------------------------

client = Groq(api_key=api_key)


# --------------------------------
# Load portfolio
# --------------------------------

with open("portfolio_knowledge.json", "r", encoding="utf-8") as file:
    portfolio = json.load(file)


portfolio_content = portfolio["content"]


# --------------------------------
# Split portfolio into sections
# --------------------------------

sections = [
    section.strip()
    for section in portfolio_content.split("\n\n")
    if section.strip()
]


print("Total sections:", len(sections))


# --------------------------------
# Create TF-IDF search
# --------------------------------

vectorizer = TfidfVectorizer()

section_vectors = vectorizer.fit_transform(sections)


# --------------------------------
# Ask question
# --------------------------------

question = input("\nAsk something about the portfolio: ")


# Convert question to vector
question_vector = vectorizer.transform([question])


# Calculate similarity
similarities = cosine_similarity(
    question_vector,
    section_vectors
)[0]


# --------------------------------
# Get top relevant sections
# --------------------------------

top_results = similarities.argsort()[-5:][::-1]


relevant_sections = []

for index in top_results:

    if similarities[index] > 0:

        relevant_sections.append(sections[index])


# --------------------------------
# Create context
# --------------------------------

context = "\n\n".join(relevant_sections)


# --------------------------------
# Ask Groq
# --------------------------------

prompt = f"""
You are an AI assistant for Avoodaiappan's portfolio.

Answer the user's question ONLY using the information
provided in the portfolio context.

Do not invent or assume information.

If the information is not available, say:

"I couldn't find that information in the portfolio."

PORTFOLIO CONTEXT:

{context}

USER QUESTION:

{question}
"""


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


# --------------------------------
# Display answer
# --------------------------------

answer = response.choices[0].message.content

print("\nAssistant:")
print(answer)