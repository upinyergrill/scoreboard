"""testing period time
"""
import period_time as pt

GAME_DATA = pt.get_game_data_from_file('exampleDataGameLive.json')
#GAME_DATA = pt.get_game_data_from_file('exampleDataGameStopped.json')

PARSED_GAME_DATA = pt.get_parsed_game_data(GAME_DATA)

GAME_TIME_AND_PERIOD = pt.get_game_time_and_period(PARSED_GAME_DATA)

print("Scorer: {}".format(pt.get_last_goal_info(GAME_DATA)))

print("Period: {}".format(GAME_TIME_AND_PERIOD['period']))

if pt.should_start_timer(PARSED_GAME_DATA) is True:
    #pt.countdown(3)
    pt.countdown(pt.get_seconds_from_string(GAME_TIME_AND_PERIOD['time']))
