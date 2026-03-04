import requests

base_url = 'https://clinicaltrials.gov/api/v2/studies'

params = {
    'query.term': 'paracetamol',
    'pageSize': 25,
}

response = requests.get(base_url, params=params)

if response.status_code != 200:
    print(f"Error! Status code: {response.status_code}")
    print("The server returned HTML instead of JSON. Check your URL.")
else:
    data = response.json()
    print(data)
