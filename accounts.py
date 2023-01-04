import requests
import json
import credentials

url = "https://api.akahu.io/v1/accounts"

response = requests.get(url, headers=credentials.headers)

parsed = json.loads(response.text)
print(json.dumps(parsed, indent=4))
