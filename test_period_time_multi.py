"""testing period time
"""
import period_time as pt
from multiprocessing import Process, Queue, Pipe
import time
import requests
import json
import array

def simulate_get_game_data(x):
    if x >= 3 and x <= 5:
        return pt.get_game_data_from_file('exampleDataGameStopped.json')
    elif x > 5:
        return pt.get_game_data_from_file('exampleDataGameLive3.json')
    else:
        return pt.get_game_data_from_file('exampleDataGameLive.json')

def get_game_data():
    #url = "https://statsapi.web.nhl.com/api/v1/game/2017020862/feed/live"
    #req = requests.get(url)
    #return req.json()
    return pt.get_game_data_from_file('exampleDataGameLive.json')

def is_period_live(time):
    try:
        pt.get_seconds_from_string(time)
        return True
    except:
        return False

def live_data(q):
    x = 0
    prev_game_data = None
    while True:
        # get live data
        #game_data = get_game_data()
        # begin simulate data # 
        x = x + 1
        print(x)
        game_data = simulate_get_game_data(x)
        # end simulate data #
        if not prev_game_data:
            # inital push of data
            prev_game_data = game_data
            q.put(game_data)
        if json.dumps(game_data) != json.dumps(prev_game_data):
            # game data has changed
            prev_game_data = game_data
            print('data changed')
            q.put(game_data)
        else:
            print('same')
            #pass
        time.sleep(5)

def start_timer_logic(q):
    timer_q = Queue()
    p = Process(target=countdown, args=(timer_q,))
    p.start()
    game_time = None
    while True:
        try:
            game_data = q.get(False)
            parsed_game_data = pt.get_parsed_game_data(game_data)
            game_time_and_period = pt.get_game_time_and_period(parsed_game_data)
            #print(game_time_and_period['time'])
            if is_period_live(game_time_and_period['time']):
                live_game_time_seconds = pt.get_seconds_from_string(game_time_and_period['time'])
                if game_time:
                    game_time_seconds = pt.get_seconds_from_string(game_time)
                else:
                    game_time_seconds = 0
                if game_time_seconds != live_game_time_seconds:
                    # time changed
                    game_time = game_time_and_period['time']
                    if pt.should_start_timer(parsed_game_data) is True:
                        # time has changed and should start timer
                        timer_q.put(live_game_time_seconds)
                    else:
                        # time has changed and should not start timer
                        timer_q.put(9999)
                else:
                    # time hasn't changed
                    pass
        except:
            #print('waiting')
            pass
        time.sleep(1)

def countdown(timer_q):
    seconds = timer_q.get()
    while True:
        try:
            seconds = timer_q.get(False)
        except:
            pass
        if seconds != 9999:
            while seconds:
                timeformat = pt.seconds_to_string(seconds)
                print('Time: ', timeformat)
                try:
                    # dosn't matter if its 9999 or new seconds
                    # it's an update to break to outer loop
                    seconds = timer_q.get(False)
                    print('received seconds: ', seconds)
                    break
                except:
                    seconds -= 1
                    time.sleep(1)
        if seconds == 0:
            print('00:00')
            break

if __name__ == '__main__':
    q = Queue()
    p1 = Process(target=live_data, args=(q,))
    p2 = Process(target=start_timer_logic, args=(q,))
    p1.start()
    p2.start()
    p1.join()
    p2.join()
    