#from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from multiprocessing import Process, Queue, Value
from flask import Flask
import json

# The Board
def board():
    ''' This will need to listen to the rest_api_queue 
    for messages to switch teams and things like that '''
    
    ''' This process need to have a sub prrocess for 
        getting game data, it will call both 
        the "next" and the "live" data URIs '''
    
    # Create Fetch NHL Data proces
    fetch_nhl_data_process = Process(target=fetch_nhl_data, args=())
    
    # Start Fetch NHL Data process
    fetch_nhl_data_process.start()
    
    # Wait for Fetch NHL Data to finish (it never will)
    #fetch_nhl_data_process.join()
    
    ''' The main function of the Board process should be waiting
        for the REST API process to send it data
        
        The process should also handle starting and stopping
        all the other sub processes for 
        getting and display data on the board '''
    while True:
        try:
            message_from_rest_api = rest_api_queue.get(False)
            ''' Need a function for processing the data from the rest api
                Probably should send an object from the rest api of the
                function and the value
                something like... 
                    {
                        "function": "changeTeam"
                        "value": 17
                    } 
                Changing the team will need to tell the fetch_nhl_data
                function to use a differnt URIs but also will need to
                tell the function for what colors to use to update. '''
        except:
            pass
    pass

# Download NHL Data
def fetch_nhl_data(team_id):
    ''' download data from the "next" URI and
        download data fro mthe "live" URI. '''
    schedule_next = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' + team_id + '?expand=team.schedule.next')
    schedule_next = (schedule_next.json())
    try:
        next_game_id = (schedule_next['teams'][0]['nextGameSchedule']['dates'][0]['games'][0]['gamePk'])
    except:
        pass
    live_game_data = requests.get('https://statsapi.web.nhl.com/api/v1/game/' + str(next_game_id) + '/feed/live')
    live_game_data = (live_game_data.json())

def determine_game_state():
    ''' This function determines the state of the game.
        The possible states are, pre, live, and post. '''
    # Download "next" URI
    # Find the next/current game from the "next" data
    # Download "live" URI
    # if game is live
        #  display live game data
    # else
        # if (the game has ended within the last 15 minutes)
            # display post game
        # if else (the next game starts in 15 minutes or less)
            # display pre game
        # else (if the game has ended more than 15 minutes ago, 
        # and the next game doesn't start in 15 minutes or less)
            # turn off the board display 
    pass

# makes the flask app work
app = Flask(__name__)

# Shared memory value
shared_memory_team_id = Value('i', 1)

@app.route('/team/<int:team_id>', methods=['GET', 'POST'])
def show_team(team_id):
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    shared_memory_team_id.value = team_id
    rtn = json.dumps({'team': shared_memory_team_id.value}, separators=(',',':'))
    return rtn

# flask cant use __name__ == '__main__'
# This is the main process
#if __name__ == '__main__':

nhl_data_queue = Queue()

nhl_data_process = Process(target=fetch_nhl_data, args=(shared_memory_team_id,))

board_process = Process(target=board, args=(nhl_data_queue,))

nhl_data_process.start()

board_process.start()
