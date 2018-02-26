import pymysql.cursors
from requests import HTTPError
from datetime import datetime
from custom_riot_wrapper import get_data
from custom_class import matche_record
from custom_class import summoner_object
connection = pymysql.connect(host='localhost',user='', password='', db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def insert_summoner(summoner):
	with connection.cursor() as cursor:
		# insert in summoners_active
		date_added = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
		active = True
		sql = "INSERT INTO `summoners_active` (`summoner_id`, `accountId`, `date_added`, `active`, `name`) VALUES (%s, %s, %s, %s, %s)"
		cursor.execute(sql, (summoner.summoner_id, summoner.accountId, date_added, active, summoner.summoner_name))	
	connection.commit()
	add_summoner_entry(summoner)

def add_summoner_entry(summoner):
	with connection.cursor() as cursor:
		# update entry in summoner_current_stats 
		sql = "INSERT INTO `summoners_current_stats` (`summoner_id`, `date_new_rank`, `date_new_tier`, `summonerLevel`, `rank`, `leagueName`, `tier`, `hotStreak`, `wins`, `losses`, `summoner_name`, `leaguePoints`) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"
		cursor.execute(sql, (summoner.summoner_id, summoner.date_new_rank, summoner.date_new_tier, summoner.summonerLevel, summoner.rank, summoner.leagueName, summoner.tier, summoner.hotStreak, summoner.wins, summoner.losses, summoner.summoner_name, summoner.leaguePoints))
	connection.commit()

def check_summoner_exist(summoner_id):
	with connection.cursor() as cursor:
		sql = "SELECT `summoner_id` FROM `summoners_active` WHERE `summoner_id` = %s"
		cursor.execute(sql, summoner_id)
		result = cursor.fetchone()
		if result:
			exist_in_db = True
		else:
			exist_in_db = False
		return exist_in_db

def logtext(message):

	timestamp = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
	channel = str(message.channel)
	guild = str(message.guild)
	author = str(message.author)
	content = str(message.content)
	print('{} [{}|{}] {}: {}'.format(timestamp, guild, channel, author.split('#')[0], content))


	with connection.cursor() as cursor:
		sql = "INSERT INTO `chat_history` (`date`, `channel`, `author`, `content`) VALUES (%s, %s, %s, %s)"
		cursor.execute(sql, (timestamp, channel, author, content))
	connection.commit()


def print_message(timestamp, channel, author, content):
	line = ('{} {} {}: {}'.format(timestamp, channel, author.split('#')[0], content))
	print(line)

def translate_rank(rank):

	if rank == 'I':
		rank = 1
	elif rank == 'II':
		rank = 2
	elif rank == 'III':
		rank = 3
	elif rank == 'IV':
		rank = 4
	elif rank == 'V':
		rank = 5
	else:
		rank = 0

	return rank

def get_summoner_id(summoner_pseudo):

	url = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}'.format(summoner_pseudo)
	me = get_data(url)
	summoner_id = me['id']
	accountId = me['accountId']
	return summoner_id, accountId



def update_lol_stats(summoner_id, summoner_pseudo):

	url = 'https://na1.api.riotgames.com/lol/league/v3/positions/by-summoner/{}'.format(summoner_id)

	my_ranked_stats = get_data(url)

	url = 'https://na1.api.riotgames.com/lol/summoner/v3/summoners/by-name/{}'.format(summoner_pseudo)
	me = get_data(url)

	if my_ranked_stats[0]['queueType'] != 'RANKED_SOLO_5x5':
		my_ranked_stats = my_ranked_stats[1]
	else:
		my_ranked_stats = my_ranked_stats[0]

 	
	summonerLevel = me['summonerLevel']
	accountId = me['accountId']

	summoner_name = summoner_pseudo
	rank = translate_rank(my_ranked_stats['rank'])
	leagueName = my_ranked_stats['leagueName']
	leaguePoints = my_ranked_stats['leaguePoints']
	tier = my_ranked_stats['tier']
	hotStreak = my_ranked_stats['hotStreak']
	wins = my_ranked_stats['wins']
	losses  = my_ranked_stats['losses']
	exist_in_db = check_summoner_exist(summoner_id)

	date_new_rank = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')
	date_new_tier = datetime.strftime(datetime.now(), '%y/%m/%d %H:%M:%S')

	summoner = summoner_object(summoner_id, summonerLevel, rank, leagueName, tier, hotStreak, wins, losses, summoner_name, leaguePoints, date_new_rank, date_new_tier, accountId)
	if exist_in_db is True:
		print('# Updating  Summoner: {}'.format(summoner_name))
		add_summoner_entry(summoner)
	else:
		print('#Adding Summoner: {}'.format(summoner_name))
		insert_summoner(summoner)

	return summoner

def get_summoner_stats(summoner_id, summoner_pseudo):

	summoner = update_lol_stats(summoner_id, summoner_pseudo)
	return summoner


def post_latest_game():
	results_list = {}
	connection = pymysql.connect(host='localhost',user='', password='', db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)

	with connection.cursor() as cursor:
		sql = "SELECT `*` FROM `summoners_active` WHERE 1"
		cursor.execute(sql)
		sum_results = cursor.fetchall()
		for account in sum_results:
			if account['active'] == 1:				
				summoner_id = account['summoner_id']
				accountId = account['accountId']
				summoner_name = account['name']

				sql2 = "SELECT `*` FROM `matches` WHERE `accountId` = %s AND `posted` = 0"
				cursor.execute(sql2, accountId)
				results = cursor.fetchall()
				for each in results:
					name = str(each['gameId'])
					if name not in results_list:
						sql3 = "UPDATE `matches` SET `posted` = 1 WHERE gameId = %s"
						cursor.execute(sql3, each['gameId'])
						connection.commit()
						results_list[name] = matche_record(summoner_name, each['gameId'],each['champion'],each['timestamp'],each['lane'],each['queue'],each['season'],each['gameMode'],each['accountId'],each['participantId'],each['win'],each['physicalDamageDealt'],each['magicDamageDealt'],each['totalDamageDealt'],each['kills'],each['assists'],each['deaths'],each['totalDamageTaken'],each['totalMinionsKilled'],each['totalPlayerScore'],each['goldEarned'],each['goldSpent'],each['posted'])			
	connection.close()
	return results_list
					
					


def get_champion_name(champion_id):
		
	with connection.cursor() as cursor:
		sql = "SELECT `champion_name` FROM `champions_infos` WHERE `champion_id` = %s"
		cursor.execute(sql, champion_id)
		result = cursor.fetchone()
		return result['champion_name']

def get_queue_name(queue):
	print(queue)
	if queue == 400:
		queue = '5v5 Draft Pick games'
	elif queue == 420:
		queue = '5v5 Ranked Solo games'
	elif queue == 430:
		queue = '5v5 Blind Pick games'
	elif queue == 440:
		queue = '5v5 Ranked Flex games'
	elif queue == 450:
		queue = '5v5 ARAM games'	
	else:
		queue = 'Not sure'

	return queue