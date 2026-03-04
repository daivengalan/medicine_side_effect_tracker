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

    aggregated = {}
    studies = data.get('studies', [])

    for study in studies:
        if study.get('hasResults'):
            adverse = study.get('resultsSection', {}).get('adverseEventsModule', {})

            if 'seriousEvents' in adverse:
                events = adverse['seriousEvents']

                for event in events:
                    stats = event.get('stats', [])
                    if stats and stats[0].get('numAtRisk', 0) > 0:
                        name = event.get('term')
                        probability = stats[0]['numAffected'] / stats[0]['numAtRisk']

                        if name in aggregated:
                            aggregated[name].append(probability)
                        else:
                            aggregated[name] = [probability]

    results = [
        {
            'side_effect_name': name,
            'side_effect_probability': sum(probabilities) / len(probabilities)
        }
        for name, probabilities in aggregated.items()
    ]

    print([side_effect for side_effect in results if side_effect['side_effect_probability'] > 0.01])