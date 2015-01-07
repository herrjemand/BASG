import json
data = {}
with open('games.json') as r:
	data = json.loads(r.read())
summ = sum([data[key]['price'] for key in data.keys()])
print('Games: ', len(data.keys()))
print('Total cost: ', round(summ, 2))
print('Median price: ', round(summ/len(data.keys()), 2))