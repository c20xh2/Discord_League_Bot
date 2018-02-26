class matche_record():
	def __init__(self,
				summoner_name,
				gameId,
				champion,
				timestamp,
				lane,
				queue,
				season,
				gameMode,
				accountId,
				participantId,
				win,
				physicalDamageDealt,
				magicDamageDealt,
				totalDamageDealt,
				kills,
				assists,
				deaths,
				totalDamageTaken,
				totalMinionsKilled,
				totalPlayerScore,
				goldEarned,
				goldSpent,
				posted):
		self.summoner_name = summoner_name
		self.gameId = gameId
		self.champion = champion
		self.timestamp = timestamp
		self.lane = lane
		self.queue = queue
		self.season = season
		self.gameMode = gameMode
		self.accountId = accountId
		self.participantId = participantId
		self.win = win
		self.physicalDamageDealt = physicalDamageDealt
		self.magicDamageDealt = magicDamageDealt
		self.totalDamageDealt = totalDamageDealt
		self.kills = kills
		self.assists = assists
		self.deaths = deaths
		self.totalDamageTaken = totalDamageTaken
		self.totalMinionsKilled = totalMinionsKilled
		self.totalPlayerScore = totalPlayerScore
		self.goldEarned = goldEarned
		self.goldSpent = goldSpent
		self.posted = posted


class summoner_object():
	def __init__(self, summoner_id, summonerLevel, rank, leagueName, tier, hotStreak, wins, losses, summoner_name, leaguePoints, date_new_rank, date_new_tier, accountId):
		self.summoner_id = summoner_id
		self.summonerLevel = summonerLevel
		self.rank = rank
		self.leagueName = leagueName
		self.tier = tier
		self.hotStreak = hotStreak
		self.wins = wins
		self.losses = losses
		self.summoner_name = summoner_name
		self.leaguePoints = leaguePoints
		self.date_new_rank = date_new_rank
		self.date_new_tier = date_new_tier
		self.accountId = accountId
