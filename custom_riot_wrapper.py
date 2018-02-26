import requests


def get_data(url):

	x_riot_token = ''
	headers = {'X-Riot-Token': x_riot_token}
	r = requests.get(url, headers=headers)
	data = r.json()
	return data
