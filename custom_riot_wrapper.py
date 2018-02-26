import requests


def get_data(url):
	with open('riot_api_key.txt','r') as apikeyfile:
		for line in apikeyfile:
			riot_api_key = line.strip()
			
	x_riot_token = riot_api_key
	headers = {'X-Riot-Token': x_riot_token}
	r = requests.get(url, headers=headers)
	data = r.json()
	return data
