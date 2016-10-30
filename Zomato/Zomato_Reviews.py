import requests
from bs4 import BeautifulSoup
import json

res_ids = [16817448, 16825829, 16830337, 16810579, 16820124, 16813268, 16831684, 16812432, 16819715, 16819859, 16825776, 16830386, 16823843, 16821118, 16825758, 16811997, 16810917, 16809318, 16822116, 16808460, 16807372, 16817969, 16822176, 16825707, 16825525, 16819015, 16814205, 16831308, 16816273, 16824505, 16825724, 16808843, 16806930, 16814344, 16807074, 16807448, 16821302, 16820386, 16824260, 16823533, 16834143, 16807622, 16832819, 16818845, 16834710, 16826001, 16812554, 16822512, 16832638, 16814839, 16808349, 16817772, 16830282, 16819026, 16825054, 16810374, 16835820, 16810509, 16813342, 16818827, 16825642, 16833760, 16813775, 16814832, 16824393, 16837244, 16825809, 16824394, 16834502, 16819172, 16817459, 16834158, 16816171, 16837045, 16814028, 16818241, 16834498, 16833253, 16825812, 16823852, 16807555, 16808828, 16808344, 16821120, 16834618, 16818299, 16810520, 16809791, 16808461, 16809550, 16835062, 16810375, 16811523, 16809593, 16808305, 16835804, 16825705, 16808534, 16832584, 16833817];


url = "https://www.zomato.com/php/social_load_more.php";
i = 1
for res_id in res_ids:
	print res_id
	data = {
		'entity_id' : res_id, #This is the res_id, loop over this value
		'profile_action' :'reviews-dd',  # 'reviews-top' was the value before, and was getting popular reviews
		'page' : 2, #You can either use page or limit to get more reviews. This is probably something that's being used on the client-side to render.
		'limit' : 10
	}

	headers = {
		'authority' : 'www.zomato.com',
		'method': 'POST',
		'path': '/php/social_load_more.php',
		'scheme': 'https',
		'accept': '*/*',
		'accept-encoding': 'gzip, deflate, br',
		'accept-language': 'en-US,en;q=0.8',
		'content-length': '56',
		'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
		'cookie': 'dpr=2; zl=en; fbtrack=30c97c8bae903f6aa170bf23a79060b2; fbm_288523881080=base_domain=.zomato.com; gsc1=0; al=0; lty=subzone; ltv=5106; zone=5200; PHPSESSID=d180dfb81091195bb4222f220cf13c6dd1a8f3f9; zhli=1; squeeze=bb082379aa0b8d7eeed7c0cc301fd179; orange=5975756; fbsr_288523881080=l_JJ2BvIe2LKH21G0IOULFF15a8x8M4w7J_oJk4-2es.eyJhbGdvcml0aG0iOiJITUFDLVNIQTI1NiIsImNvZGUiOiJBUUNwLVlQZ2NYeTVGcUpQOThLNlgxUG1XS0VmZDdwSEN2WVdjWHk3ck1kcTZiM1pmVGpGcWFYSlo5WVd5VnVWdXR5a3FqU1ZSU2tFWFo5Qm5hRkx5Zkw2LVVRUWZnNEgybU5oZ0ZQOVE4RnZMSGNxVVNlX1E1WkNob2wwQmJVb3ZOam9NUXZNdmdjRUxKMUxqcVZmSUlzc3FWQ0IwNmNfVUhEZEIyd0RlR0w0WWpVZmhERGlrRU45VzdUc0dTdUlHZWZNUE9MSWpyWktDV003SE0xWVcyV0tLOWxwdFBYQlZjajJLdHJoOTdSejBIMnhxa2RYaXlCajg2QzNpbVBrbHp5dFQ4OUxwU0ppcWswQmlqY3lHbXR4SWVJMHZGbk5ZNGdZV2VDQndZR3JMUVB1WWtwRGtUZlNUQTVpNW03R2p3YXdHaEFEanVXYjJKcXU5R3hDMWJqbiIsImlzc3VlZF9hdCI6MTQ3Nzc5NTYxMCwidXNlcl9pZCI6IjEwMjAzNDkyMjU0NzM0NDM2In0; fbcity=1; _ga=GA1.2.1537756356.1474289804; __jpuri=https%3A//www.zomato.com/ncr/ardor-2-1-connaught-place-new-delhi; ak_bmsc=07099EB0AB984F42A1913909461B863B1739459FDA4100006E5B1558CCBD602E~plGf0QhgC0FEoN4NNYgzpOVqy4D+q8mePf5DSdSGUVchcYRPXUVuKYcCdjqLraThQD0xdlWf7OMDl9vsyaXw1DBQdEeMr+w7nIMfcgdZo5HHsSb/8OwlTBhHSUiKLOsHNglWYhu9ExU+NzTx3tzaKof1qqQ2r1+RCr83RDmix9tvBg2rjSYoDff5RRXzibqJlETAhrHpH3nKkKsaUNhxmbZw==',
		'origin': 'https://www.zomato.com',
		'referer': 'https://www.zomato.com/',
		'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36',
		'x-requested-with': 'XMLHttpRequest'
	}

	r = requests.post(url, headers=headers, data=data)
	data= json.loads(r.text)
	filename = "dump" + str(i) + ".txt"
	f = open(filename,"w")
	#print(data['html'])
	#print("--------------------")
	#f.write(data['html'])
	json.dump(data,f)
	f.close()
	i = i+1

'''
soup= BeautifulSoup(r.text, "lxml")
print(soup)
'''

