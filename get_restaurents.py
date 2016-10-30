import json
from pprint import pprint

with open('restaurents.json') as data_file:    
    data = json.load(data_file)

res_id = []
for k in data[u'restaurants']:
	for key in k.keys():
		if 'R' in k[key].keys():
			res_id.append(k[key]['R']['res_id'])

print res_id
	