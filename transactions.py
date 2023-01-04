import requests
import credentials
import datetime
import json

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=6)

url = f"https://api.akahu.io/v1/transactions?start={yesterday.isoformat()}&end={now.isoformat()}"
#url = f"https://api.akahu.io/v1/transactions?start=2022-01-01"
#url = f"https://api.akahu.io/v1/transactions"

print(url)
response = requests.get(url, headers=credentials.headers)
parsed = json.loads(response.text)

print(json.dumps(parsed, indent=4))