import json
import pymysql
data = json.load(open('champions.txt'))
i = 1

with open('db_credit.txt', 'r') as db_credit:
	for line in db_credit:
		user = line.split(':')[0]
		password = line.split(':')[1]
		
connection = pymysql.connect(host='localhost',user= user, password=password, db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def insert_champ(champion_name, champion_id):
	with connection.cursor() as cursor:
		# insert in summoners_active
		sql = "INSERT INTO `champions_infos` (`champion_id`, `champion_name`) VALUES (%s, %s)"
		cursor.execute(sql, (champion_id, champion_name))	
	connection.commit()



while i < 1000:
	try:

		champion_name = (data['data'][str(i)]['name'])
		champion_id = (data['data'][str(i)]['id'])
		print(i)
		insert_champ(champion_name, champion_id)
		i += 1
	except:
		i += 1
		pass


