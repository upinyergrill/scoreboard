"""period and time
"""
from __future__ import print_function
import json
import time


"""
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
        - set time to intermissionTimeRemaining
        - set period to InT
        - start counter at intermissionTimeRemaining
            intermissionTimeRemaining is in seconds
    - else if (abstractGameState == Live) && (intermissionTimeRemaining == 0) (game is live)
        - set period to currentPeriodOrdinal
        - get all stoppage events
        - stoppage.count > 0
            - find the last stoppage
            - if stoppage in the same period
                - if currentPeriodTimeRemaining == periodTimeRemaining +/- 1 second
                  i saw be periodTimeRemaining 2 while currentPeriodTimeRemaining was 1
                    - set time to periodTimeRemaining
                - else
                    - start counter at currentPeriodTimeRemaining
        - else
            - start counter at currentPeriodTimeRemaining
"""


def get_seconds_from_string(time_str):
    """convert minute:second string time to int seconds
    print get_seconds_from_string('10:45')
    print get_seconds_from_string('20:00')
    print get_seconds_from_string('03:14')
    https://stackoverflow.com/a/6402859/1469690
    """
    minute, second = time_str.split(':')
    return int(minute) * 60 + int(second)


def get_game_data_from_file(file_name):
    """imports json data
    """
    return json.load(open(file_name))


def get_all_stoppage(game_data):
    """gets all stoppage events from unparsed game data
    """
    all_plays = game_data['liveData']['plays']['allPlays']

    # Will return [] if none
    stoppage = [d for d in all_plays if d['result']['event'] == 'Stoppage']

    '''
    prices = {
        'ACME': 45.23,
        'AAPL': 612.78,
        'IBM': 205.55,
        'HPQ': 37.20,
        'FB': 10.75
    }

    # Make a dictionary of all prices over 200
    one = {key: value for key, value in prices.items() if value > 200}

    # Make a dictionary of tech stocks
    tech_names = {'AAPL', 'IBM', 'HPQ', 'MSFT'}
    two = {key: value for key, value in prices.items() if key in tech_names}
    '''

    return stoppage


def get_parsed_game_data(game_data):
    """parses game data
    """
    game = {}

    game['abstractGameState'] = (
        game_data['gameData']['status']['abstractGameState']
    )

    game['currentPeriod'] = (
        game_data['liveData']['linescore']['currentPeriod']
    )

    game['currentPeriodOrdinal'] = (
        game_data['liveData']['linescore']['currentPeriodOrdinal']
    )

    if (game_data['liveData']['linescore']['currentPeriodTimeRemaining'] == 'END'):
        game['currentPeriodTimeRemaining'] = '00:00'
    else:
        game['currentPeriodTimeRemaining'] = (
            game_data['liveData']['linescore']['currentPeriodTimeRemaining']
        )

    game['intermissionTimeRemaining'] = (
        game_data['liveData']['linescore']['intermissionInfo']['intermissionTimeRemaining']
    )

    game['stoppage'] = (
        get_all_stoppage(game_data)
    )

    return game


def get_game_time_and_period(game_data):
    """figures out what the time and period should be
    uses parsed game data from get_parsed_game_data
    """
    info = {'time': '', 'period': ''}

    # Game has not started
    if game_data['abstractGameState'] == 'Preview':
        info['period'] = "PRE"
        info['time'] = '00:00'

    # Game over
    elif game_data['abstractGameState'] == 'Final':
        info['period'] = "END"
        info['time'] = '00:00'

    # Intermission
    elif (game_data['abstractGameState'] == 'Live' and
          game_data['intermissionTimeRemaining'] != 0):
        info['period'] = "InT"
        info['time'] = seconds_to_string(game_data['intermissionTimeRemaining'])

    # End of period
    elif (game_data['abstractGameState'] == 'Live' and
          game_data['intermissionTimeRemaining'] == 0 and
          game_data['currentPeriodTimeRemaining'] == 'END'):
        info['period'] = game_data['currentPeriodOrdinal']
        info['time'] = '00:00'

    # Game is live
    elif (game_data['abstractGameState'] == 'Live' and
          game_data['intermissionTimeRemaining'] == 0 and
          game_data['currentPeriodTimeRemaining'] != 'END'):
        info['period'] = game_data['currentPeriodOrdinal']
        info['time'] = game_data['currentPeriodTimeRemaining']

    return info


def should_start_timer(game_data):
    """determines if the timer should start
    return boolean
    """
    print('should_start_timer begin')
    if game_data['intermissionTimeRemaining'] >= 1:
        print('should_start_timer in intermission')
        return True
    if len(game_data['stoppage']) >= 1:
        # print('has stoppage')
        latest_stoppage = game_data['stoppage'][-1]
        latest_stoppage_period = latest_stoppage['about']['period']
        latest_stoppage_time_remaining = latest_stoppage['about']['periodTimeRemaining']

        if game_data['currentPeriod'] == latest_stoppage_period:
            print('last stopage was in this period')
            time_remaining_seconds = get_seconds_from_string(
                game_data['currentPeriodTimeRemaining']
            )
            print('time_remaining_seconds', time_remaining_seconds)
            stoppage_time_remaining_seconds = get_seconds_from_string(
                latest_stoppage_time_remaining
            )
            print('stoppage_time_remaining_seconds', stoppage_time_remaining_seconds)
            if (time_remaining_seconds == stoppage_time_remaining_seconds or
                    time_remaining_seconds == (stoppage_time_remaining_seconds + 1) or
                    time_remaining_seconds == (stoppage_time_remaining_seconds - 1)):
                print('don\'t start timer, game is stopped')
                return False
            else:
                # game has resume since last stoppage
                print('start timer')
                return True
        else:
            print('start timer, last stoppage was not in current period')
            return True
    else:
        print('start timer, no stoppage yet in game')
        return True


def seconds_to_string(seconds):
    """converts seconds to 00:00 format
    """
    mins, secs = divmod(seconds, 60)
    timeformat = '{:02d}:{:02d}'.format(mins, secs)
    return timeformat


def countdown(seconds):
    """countdown from stackoverlow
    https://stackoverflow.com/a/25189629/1469690
    """
    while seconds:
        timeformat = seconds_to_string(seconds)
        print(timeformat)
        time.sleep(1)
        seconds -= 1
    print('00:00')


def get_last_goal_info(game_data):
    """ gets the last goal
    """
    all_plays = game_data['liveData']['plays']['allPlays']
    goal_info = [d for d in all_plays if d['result']['event'] == 'Goal']
    if goal_info:
        goal_info = goal_info[-1]
        player = [d for d in goal_info['players'] if d['playerType'] == 'Scorer']
        return player
