import sys
import json
import requests
import datetime
import pytz, dateutil.parser

#now = datetime.datetime.now()
#date = now.strftime("%Y-%m-%d")

teamId = '5'
games = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + teamId + '?expand=team.schedule.next&expand=team.schedule.previous')
parsed_games = (games.json())

#nextgamedate = (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['date'])
#if date == nextgamedate:
gamePK = (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gamePk'])
#else:
#gamePK = (parsed_games['teams'][0]['previousGameSchedule']['dates'][0]['games'][0]['gamePk'])

gameinfo = requests.get('https://statsapi.web.nhl.com/api/v1/game/' + str(gamePK) + '/feed/live')
parsed_gameinfo = (gameinfo.json())

def teamID():
	return teamId

def awayTeam():
	return (parsed_gameinfo['gameData']['teams']['away']['abbreviation'])

def homeTeam():
	return (parsed_gameinfo['gameData']['teams']['home']['abbreviation'])

def awayScore():
	return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']))

def homeScore():
	return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']))

def period():
	return (parsed_gameinfo['liveData']['linescore']['currentPeriodOrdinal'])

def timeLeft():
	return (parsed_gameinfo['liveData']['linescore']['currentPeriodTimeRemaining'])

def awaySog():
	return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots']))

def homeSog():
	return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots']))

def gameStatus():
	return (parsed_gameinfo['gameData']['status']['abstractGameState'])

def awayWin():
	return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['wins'])

def awayLose():
	return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['losses'])

def awayOtl():
	return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['ot'])

def homeWin():
        return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['wins'])

def homeLose():
        return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['losses'])

def homeOtl():
        return (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['ot'])

def gameTime():
	gamedate = (parsed_games['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate'])
	utctime = dateutil.parser.parse(gamedate)
	return (utctime.astimezone(pytz.timezone("US/Eastern")))

def intTime():
	intTime = (parsed_gameinfo['liveData']['linescore']['intermissionInfo']['intermissionTimeRemaining'])
	return (str(datetime.timedelta(seconds=intTime)).split(':')[1] + ":" + str(datetime.timedelta(seconds=intTime)).split(':')[2])

def awaySkaters():
	return (parsed_gameinfo['liveData']['linescore']['teams']['away']['numSkaters'])

def homeSkaters():
	return (parsed_gameinfo['liveData']['linescore']['teams']['home']['numSkaters'])

def awayPowerPlay():
	return (parsed_gameinfo['liveData']['linescore']['teams']['away']['powerPlay'])

def homePowerPlay():
	return (parsed_gameinfo['liveData']['linescore']['teams']['home']['powerPlay'])

def awayHits():
	return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['hits']))

def homeHits():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['hits']))

def awayBlocks():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['blocked']))

def homeBlocks():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['blocked']))

def awayTakeaways():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['takeaways']))

def homeTakeaways():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['takeaways']))

def awayGiveaways():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['giveaways']))

def homeGiveaways():
        return ("{0:0=2d}".format(parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['giveaways']))

def awayFOWins():
        return (parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage'])

def homeFOWins():
        return (parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage'])

def awayPP():
	converted = (parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayGoals'])
	total = (parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayOpportunities'])
	return (str(converted).split('.')[0] + "-" + str(total).split('.')[0])

def homePP():
        converted = (parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayGoals'])
        total = (parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayOpportunities'])
        return (str(converted).split('.')[0] + "-" + str(total).split('.')[0])

def goalScored():
	eventData = (parsed_gameinfo['liveData']['plays']['allPlays'])
	for x in eventData:
		if x['result']['event'] == 'Goal':
			goalData = (x['result']['description'])
			print(goalData)
