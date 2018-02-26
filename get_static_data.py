import pymysql.cursors
from time import sleep
from custom_riot_wrapper import get_data

with open('db_credit.txt', 'r') as keyfile:
	for line in keyfile:
		user = line.split(':')[0]
		password = line.split(':')[1]

connection = pymysql.connect(host='localhost',user=user, password=password, db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

url = 'https://na1.api.riotgames.com/lol/static-data/v3/champions?locale=en_US&champListData=info&dataById=false'

data = get_data(url)

for each in data['data']:
	print(each)
