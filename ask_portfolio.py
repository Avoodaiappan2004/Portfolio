import os
import json

from dotenv import load_dotenv
from groq import Groq


# Load .env
load_dotenv()

# Get Groq API key
api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("Groq API key not found!")
    exit()


# Create Groq client
client = Groq(api_key=api_key)


# Load portfolio knowledge
with open("portfolio_knowledge.json", "r", encoding="utf-8") as file:
    portfolio = json.load(file)


portfolio_content = portfolio["content"]


# Ask user a question
question = input("\nAsk something about the portfolio: ")


# Create prompt
prompt = f"""
You are a portfolio assistant.

You must answer the user's question ONLY using the portfolio
information provided below.

Do not invent information.

If the answer is not available in the portfolio, say:
"I couldn't find that information in the portfolio."

PORTFOLIO INFORMATION:
{portfolio_content}

USER QUESTION:
{question}
"""


# Send to Groq
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


# Display answer
answer = response.choices[0].message.content

print("\nAssistant:")
print(answer)