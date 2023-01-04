import requests
import credentials

url = "https://api.akahu.io/v1/me"

response = requests.get(url, headers=credentials.headers)

print(response.text)