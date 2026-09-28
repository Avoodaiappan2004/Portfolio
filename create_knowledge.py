import json

# Read extracted portfolio data
with open("portfolio_data.txt", "r", encoding="utf-8") as file:
    portfolio_data = file.read()

# Create knowledge structure
knowledge = {
    "source": "https://avoodport.netlify.app/",
    "content": portfolio_data
}

# Save as JSON
with open("portfolio_knowledge.json", "w", encoding="utf-8") as file:
    json.dump(knowledge, file, indent=4, ensure_ascii=False)

print("Portfolio knowledge created successfully!")

print("File created:")
print("portfolio_knowledge.json")