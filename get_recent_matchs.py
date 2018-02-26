import pymysql.cursors
from time import sleep
from requests import HTTPError
from datetime import datetime
from custom_riot_wrapper import get_data
from custom_function import get_summoner_id
from custom_function import update_lol_stats
from custom_class import matche_record



connection = pymysql.connect(host='localhost',user='', password='', db='discord_bot',charset='utf8mb4', cursorclass=pymysql.cursors.DictCursor)


def get_game_data(gameId):
	url = 'https://na1.api.riotgames.com/lol/match/v3/matches/{}'.format(gameId)
	game_data = get_data(url)
	return game_data


def get_recent_matchs(accountId):
	url = 'https://na1.api.riotgames.com/lol/match/v3/matchlists/by-account/{}/recent'.format(accountId)
	data = get_data(url)
	return data


def check_exist_match(gameId):
	with connection.cursor() as cursor:
		sql = "SELECT `gameId` FROM `matches` WHERE `gameId` = %s"
		cursor.execute(sql, gameId)
		result = cursor.fetchone()
		if result:
			exist_in_db = True
		else:
			exist_in_db = False
		return exist_in_db

def insert_match(matche_infos):
	with connection.cursor() as cursor:
		sql = "INSERT INTO `matches` (`summoner_name`,`gameId`,`champion`,`timestamp`,`lane`,`queue`,`season`,`gameMode`,`accountId`,`participantId`,`win`,`physicalDamageDealt`,`magicDamageDealt`,`totalDamageDealt`,`kills`,`assists`,`deaths`,`totalDamageTaken`,`totalMinionsKilled`,`totalPlayerScore`,`goldEarned`,`goldSpent`,`posted`) VALUES (%s, %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
		cursor.execute(sql, (matche_infos.summoner_name, matche_infos.gameId, matche_infos.champion, matche_infos.timestamp, matche_infos.lane, matche_infos.queue, matche_infos.season, matche_infos.gameMode, matche_infos.accountId, matche_infos.participantId, matche_infos.win, matche_infos.physicalDamageDealt, matche_infos.magicDamageDealt, matche_infos.totalDamageDealt, matche_infos.kills, matche_infos.assists, matche_infos.deaths, matche_infos.totalDamageTaken, matche_infos.totalMinionsKilled, matche_infos.totalPlayerScore, matche_infos.goldEarned, matche_infos.goldSpent, matche_infos.posted))	
	connection.commit()

with connection.cursor() as cursor:
	sql = "SELECT `*` FROM `summoners_active` WHERE 1"
	cursor.execute(sql)
	results = cursor.fetchall()
	for result in results:
		accountId = result['accountId']
		summoner_id = result['summoner_id']
		summoner_name = result['name']

		data = get_recent_matchs(accountId)

		for matche in data['matches']:
			sleep(1)
			gameId = matche['gameId']
			champion = matche['champion']
			timestamp = matche['timestamp']
			lane = matche['lane']
			queue = matche['queue']
			season = matche['season']

			exist_in_db = check_exist_match(gameId) 

			if exist_in_db is True:
				pass
			else:		
				game_data = get_game_data(matche['gameId'])
				gameMode = game_data['gameMode']

				# Trouve le participant ID
				for participant in game_data['participantIdentities']:
					if (participant['player']['accountId']) == accountId:
						accountId = participant['player']['accountId']
						participantId = participant['participantId']
						break

				# Trouve les stats du participant
				for participant in game_data['participants']:
					if participant['participantId'] == participantId:
						win = participant['stats']['win']

						physicalDamageDealt = participant['stats']['physicalDamageDealt']
						magicDamageDealt = participant['stats']['magicDamageDealt']
						totalDamageDealt = participant['stats']['totalDamageDealt']

						kills = participant['stats']['kills']
						assists = participant['stats']['assists']
						deaths = participant['stats']['deaths']
						
						totalDamageTaken = participant['stats']['totalDamageTaken']

						totalMinionsKilled = participant['stats']['totalMinionsKilled']
						totalPlayerScore = participant['stats']['totalPlayerScore']
						goldEarned = participant['stats']['goldEarned']
						goldSpent = participant['stats']['goldSpent']
						
						posted  = False
						matche_infos = matche_record(summoner_name, gameId, champion, timestamp, lane, queue, season, gameMode, accountId, participantId, win, physicalDamageDealt, magicDamageDealt, totalDamageDealt, kills, assists, deaths, totalDamageTaken, totalMinionsKilled, totalPlayerScore, goldEarned, goldSpent, posted)
						print('[+] Adding matche to DB:{}'.format(matche_infos.gameId))
						try:
							insert_match(matche_infos)
						except:
							pass