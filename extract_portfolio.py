import requests
from bs4 import BeautifulSoup

url = "https://avoodport.netlify.app/"

# Fetch website
response = requests.get(url)

print("Status:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Remove unnecessary HTML elements
for element in soup(["script", "style", "noscript"]):
    element.decompose()

# Extract visible text
text = soup.get_text(separator="\n")

# Clean empty lines
lines = []

for line in text.splitlines():
    line = line.strip()

    if line:
        lines.append(line)

# Join cleaned content
clean_text = "\n".join(lines)

# Save to file
with open("portfolio_content.txt", "w", encoding="utf-8") as file:
    file.write(clean_text)

print("Portfolio content extracted successfully!")

print("\nFirst 2000 characters:\n")
print(clean_text[:3000])