import pymysql.cursors
from time import sleep
from requests import HTTPError
from datetime import datetime
from custom_riot_wrapper import get_data
from custom_function import get_summoner_id
from custom_function import update_lol_stats
from custom_class import matche_record

with open('db_credit.txt', 'r') as db_credit:
	for line in db_credit:
		user = line.split(':')[0]
		password = line.split(':')[1]
		
connection = pymysql.connect(host='localhost',user= user, password=password, db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
	sql = "SELECT `*` FROM `summoners_active` WHERE 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	for result in results:
		accountId = result['accountId']
		summoner_id = result['summoner_id']
		summoner_name = result['name']
		update_lol_stats(summoner_id, summoner_name)


