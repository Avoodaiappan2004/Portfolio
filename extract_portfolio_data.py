import requests
from bs4 import BeautifulSoup

url = "https://avoodport.netlify.app/"

# Fetch website
response = requests.get(url)

print("Status:", response.status_code)

# Parse HTML
soup = BeautifulSoup(response.text, "html.parser")

# Remove unnecessary elements
for element in soup(["script", "style", "noscript"]):
    element.decompose()

# -----------------------------
# Extract text
# -----------------------------

lines = []

for line in soup.get_text(separator="\n").splitlines():
    line = line.strip()

    if line:
        lines.append(line)

clean_text = "\n".join(lines)


# -----------------------------
# Extract links
# -----------------------------

links = []

for a in soup.find_all("a", href=True):

    link_text = a.get_text(" ", strip=True)
    link_url = a["href"]

    links.append({
        "text": link_text,
        "url": link_url
    })


# -----------------------------
# Save everything
# -----------------------------

with open("portfolio_data.txt", "w", encoding="utf-8") as file:

    file.write("===== PORTFOLIO CONTENT =====\n\n")

    file.write(clean_text)

    file.write("\n\n\n===== PORTFOLIO LINKS =====\n\n")

    for link in links:

        file.write("Link Text: " + link["text"] + "\n")
        file.write("URL: " + link["url"] + "\n")
        file.write("-" * 60 + "\n")


print("Portfolio data extracted successfully!")

print("\nTotal text characters:", len(clean_text))

print("Total links found:", len(links))

print("\n===== FIRST 1000 CHARACTERS =====\n")
print(clean_text[:1000])

print("\n===== LINKS =====\n")

for link in links:
    print(link["text"], "->", link["url"])