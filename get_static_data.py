import pymysql.cursors
from time import sleep
import requests


def get_data(url):

	x_riot_token = ''
	headers = {'X-Riot-Token': x_riot_token}
	r = requests.get(url, headers=headers)
	data = r.json()
	return data

connection = pymysql.connect(host='localhost',user='', password='', db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champListData=info&dataById=false'

data = get_data(url)

for each in data['data']:
	print(each)
