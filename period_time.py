'''
    - get live data
    - parse currentPeriod
    - parse currentPeriodOrdinal
    - parse currentPeriodTimeRemaining
    - parse intermissionTimeRemaining

    - if abstractGameState == Preview (before the game starts)
        - set time to 00:00
        - set period to PRE
    - else if abstractGameState == Final (is the game over)
        - set time to 00:00
         - set period to END
    - else if (abstractGameState == Live) && (intermissionTimeRemaining != 0) (intermission)
        - set time to 00:00
        - set period to InT
    - else if (abstractGameState == Live) && (intermissionTimeRemaining == 0) (game is live)
        - set period to currentPeriodOrdinal
        - get all stoppage events
        - stoppage.count > 0
            - find the last stoppage
            - is stoppage in the same period
                - if currentPeriodTimeRemaining == periodTimeRemaining +/- 1 second
                  i saw be periodTimeRemaining 2 while currentPeriodTimeRemaining was 1
                    - set time to periodTimeRemaining
                - else
                    - start counter at currentPeriodTimeRemaining
        - else
            - start counter at currentPeriodTimeRemaining
'''
import json


def get_game_data_from_file(file_name):
    """imports json data
    """
    return json.load(open(file_name))


def get_parsed_game_data(game_data):
    """parses game data
    """
    game = {}

    game['abstractGameState'] = game_data['gameData']['status']['abstractGameState']

    game['currentPeriodOrdinal'] = (
        game_data['liveData']['linescore']['currentPeriodOrdinal'])

    game['currentPeriodTimeRemaining'] = (
        game_data['liveData']['linescore']['currentPeriodTimeRemaining'])

    game['intermissionTimeRemaining'] = (
        game_data['liveData']['linescore']['intermissionInfo']['intermissionTimeRemaining']
    )

    return game


def get_game_time_and_period(game_data):
    """figures out what the time and period should be
    """
    info = {'time': '', 'period': ''}

    if game_data['abstractGameState'] == 'Preview':
        info['time'] = '00:00'
        info['period'] = "PRE"

    elif game_data['abstractGameState'] == 'Final':
        info['time'] = '00:00'
        info['period'] = "END"

    elif (game_data['abstractGameState'] == 'Live' and
          game_data['intermissionTimeRemaining'] != 0):
        info['time'] = '00:00'
        info['period'] = "InT"

    elif (game_data['abstractGameState'] == 'Live' and
          game_data['intermissionTimeRemaining'] == 0):
        info['time'] = game_data['currentPeriodTimeRemaining']
        info['period'] = game_data['currentPeriodOrdinal']

    return info

GAME_DATA = get_game_data_from_file('exampleDataGameLive.json')

PARSED_GAME_DATA = get_parsed_game_data(GAME_DATA)

GAME_TIME_AND_PERIOD = get_game_time_and_period(PARSED_GAME_DATA)

print GAME_TIME_AND_PERIOD
