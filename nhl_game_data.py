import time
import datetime
import pytz, dateutil.parser

def get_all_stoppage(game_data):
    """gets all stoppage events from unparsed game data
    """
    all_plays = game_data['liveData']['plays']['allPlays']

    # Will return [] if none
    return [d for d in all_plays if d['result']['event'] == 'Stoppage']

def get_all_goals(game_data):
    """gets all goal events from unparsed game data
    """
    all_plays = game_data['liveData']['plays']['allPlays']

    # Will return [] if none
    return [d for d in all_plays if d['result']['event'] == 'Goal']

def get_parsed_live_game_data(game_data):
    """parses live game data
    """
    game = {}

    game['awayTeam'] = (
        game_data['gameData']['teams']['away']['abbreviation']
    )

    game['homeTeam'] = (
        game_data['gameData']['teams']['home']['abbreviation']
    )

    game['awayScore'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['goals']
    )

    game['homeScore'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['goals']
    )

    game['awaySog'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['shots']
    )

    game['homeSog'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['shots']
    )

    game['awaySkaters'] = (
        game_data['liveData']['linescore']['teams']['away']['numSkaters']
    )

    game['homeSkaters'] = (
        game_data['liveData']['linescore']['teams']['home']['numSkaters']
    )

    game['awayPowerPlay'] = (
        game_data['liveData']['linescore']['teams']['away']['powerPlay']
    )

    game['homePowerPlay'] = (
        game_data['liveData']['linescore']['teams']['home']['powerPlay']
    )

    game['awayHits'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['hits']
    )

    game['homeHits'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['hits']
    )

    game['awayBlocked'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['blocked']
    )

    game['homeBlocked'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['blocked']
    )

    game['awayTakeaways'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['takeaways']
    )

    game['homeTakeaways'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['takeaways']
    )

    game['awayGiveaways'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['giveaways']
    )

    game['homeGiveaways'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['giveaways']
    )

    game['awayFoWins'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['faceOffWinPercentage']
    )

    game['homeFoWins'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['faceOffWinPercentage']
    )

    game['awayPowerPlayConverted'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayGoals']
    )

    game['homePowerPlayConverted'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayGoals']
    )

    game['awayPowerPlayTotal'] = (
        game_data['liveData']['boxscore']['teams']['away']['teamStats']['teamSkaterStats']['powerPlayOpportunities']
    )

    game['homePowerPlayTotal'] = (
        game_data['liveData']['boxscore']['teams']['home']['teamStats']['teamSkaterStats']['powerPlayOpportunities']
    )

    game['gameState'] = (
        game_data['gameData']['status']['abstractGameState']
    )

    game['currentPeriod'] = (
        game_data['liveData']['linescore']['currentPeriod']
    )

    game['currentPeriodOrdinal'] = (
        game_data['liveData']['linescore']['currentPeriodOrdinal']
    )

    game['currentPeriodTimeRemaining'] = (
        game_data['liveData']['linescore']['currentPeriodTimeRemaining']
    )

    game['intermissionTimeRemaining'] = (
        game_data['liveData']['linescore']['intermissionInfo']['intermissionTimeRemaining']
    )

    game['stoppage'] = (
        get_all_stoppage(game_data)
    )

    game['goals'] = (
        get_all_goals(game_data)
    )

    return game

def get_parsed_pre_game_data(game_data):
    """parses pre game data
    """
    game = {}

    game['awayWin'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['wins']
    )

    game['homeWin'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['wins']
    )

    game['awayLoss'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['losses']
    )

    game['homeLoss'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['losses']
    )

    game['awayOtl'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['away']['leagueRecord']['ot']
    )

    game['homeOtl'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['teams']['home']['leagueRecord']['ot']
    )

    game['gameDateTime'] = (
        game_data['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gameDate']
    )

    return game

def format_game_datetime(date_time):
    '''Return the date time value derived from UTC and converted to local timezone
    Example return: Thu, Feb 2nd, 07:30PM
    '''
    utc_time = dateutil.parser.parse(date_time)
    local_time = (utc_time.astimezone(pytz.timezone("US/Eastern")))
    return local_time.strftime('%a, %b %d, %I:%M%p')

def format_power_plays(converted, total):
    '''Return formatted converted powerplays over total powerplay opportunities
    Example return: 0-2
    '''
    return (str(converted).split('.')[0] + "-" + str(total).split('.')[0])
