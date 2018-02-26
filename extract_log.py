import pymysql.cursors

connection = pymysql.connect(host='localhost',user='', password='', db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

with connection.cursor() as cursor:
	# Read a single record
	sql = "SELECT `*` FROM `chat_history` WHERE 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	for result in results:
		print(result)