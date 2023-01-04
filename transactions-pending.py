import requests
import credentials
import datetime
import json

now = datetime.datetime.now()
yesterday = now - datetime.timedelta(days=5)

url = f"https://api.akahu.io/v1/transactions/pending?start={yesterday.isoformat()}&end={now.isoformat()}"

print(url)
response = requests.get(url, headers=credentials.headers)
parsed = json.loads(response.text)

print(json.dumps(parsed, indent=4))