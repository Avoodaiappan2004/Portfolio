import requests

url = "https://avoodport.netlify.app/"

response = requests.get(url)

print("Status:", response.status_code)
print("Content length:", len(response.text))

print("\nFirst 1000 characters:\n")
print(response.text[:1000])