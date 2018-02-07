import sys
import json
import requests
import datetime

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

teamId = '14'
games = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' +
                     teamId + '?expand=team.schedule.next&expand=team.schedule.previous')
parsed_games = (games.json())

nextgamedate = (parsed_games['teams'][0]
                ['nextGameSchedule']['dates'][0]['date'])
if date == nextgamedate:
    gamePK = (parsed_games['teams'][0]['nextGameSchedule']
              ['dates'][0]['games'][0]['gamePk'])
else:
    gamePK = (parsed_games['teams'][0]['previousGameSchedule']
              ['dates'][0]['games'][0]['gamePk'])

gameinfo = requests.get(
    'https://statsapi.web.nhl.com/api/v1/game/' + str(gamePK) + '/feed/live')
parsed_gameinfo = (gameinfo.json())


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
    return (parsed_gameinfo['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots'])


def homeSog():
    return (parsed_gameinfo['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots'])
