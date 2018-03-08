from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from multiprocessing import Value, Process, Queue, Array
from flask import Flask
import json
import time
import nhl_game_data as nhlgamedata
import nhl_board_render as nhlboardrender
from datetime import datetime

''' su
    export FLASK_APP=flask_example.py
    python3 -m flash run
'''

# The REST API
def rest_api(rest_api_queue):
    ''' This will use Flask REST API
        At a bare minimum it will have a route called
        /team/:id where you can post to the int value
        for the team that you would like to display
        When a valid team id is matched, then it will send
        a message via the rest_api_queue to the Board process '''
    pass

# The Board
def board(rest_api_queue):
    ''' The main function of the Board process should be waiting
        for the REST API process to send it data
        
        The process should also handle starting and stopping
        all the other sub processes for 
        getting and display data on the board '''
    # Create the process for running the board
    #rest_api_queue = Queue()
    #board_process = Process(target=board, args=(rest_api_queue,))
    #board_process.start()

    # RGBMatrix Options
    options = RGBMatrixOptions()
    options.rows = 32
    options.chain_length = 2
    options.brightness = 30
    options.gpio_slowdown = 2
    options.drop_privileges = 0

    matrix = RGBMatrix(options = options)
    font = graphics.Font()
    font.LoadFont('Assets/tom-thumb.bdf')
    team_colors = json.load(open('Assets/nhlcolors.json'))
    color_white = graphics.Color(255, 255, 255)

    print('the board started')

    while True:
        try:
            game_data = rest_api_queue.get(False)
            print('omg')
            print('board got game data')
            print(game_data)
            
            #print(team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
            nhlboardrender.draw_outer_border(matrix, font, team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
            nhlboardrender.draw_time_period_border(matrix, font, team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
            
            if (game_data['gameState'] == "Preview"):
                print('should render')
                nhlboardrender.draw_away_team_pre_game(matrix, font, color_white, game_data)
                nhlboardrender.draw_home_team_pre_game(matrix, font, color_white, game_data)
                print('is it blocking code?')
                #pass
            elif(game_data['gameState'] == "Live"):
                pass
            elif(game_data['gameState'] == "Final"):
                pass
            pass
        except:
            pass
    pass

# Download NHL Data
def fetch_nhl_data():
    ''' download data from the "next" URI and
        download data fro mthe "live" URI. '''
    pass

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

def get_settings():
    """imports json data
    """
    return json.load(open('settings.json'))

def set_team_and_fetch_nhl_data(shared_mem_team, rest_api_queue):
    # At runtime set the shared_mem_team value (the settings team id)
    # to the current team id 
    current_team_id = shared_mem_team.value
    # game state get set later by fetch and parse
    game_state = None
    game_end_time = None
    # Never break from outer loop
    while True:
        '''if the game_state is not set then do this
            but if the game_state is set and 
            current_team_id does not equal shared_mem_team.value then do this
        '''
        ''' First get the pre_game_data so we can find out waht the next game is
            then get the data for that game, and determine if it is live or not
        '''
        fifteen_mintes_from_now = time.time() + 900
        if game_state is None:
            # get pre game data
            pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
            parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)
        elif game_state is not None and current_team_id != shared_mem_team.value:
            # get pre game data 
            pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
            parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)
        # we can assume game_end_time will be populated because the state is fian
        # what we want to do here is if the game has ended, this is how we tell it to get the next game
        # TODO: If game_end_time is none then this will cause an exption
        elif game_state == "Final" and game_end_time > fifteen_mintes_from_now:
            pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
            parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)
        
        # Store what the current team is for later comparison
        current_team_id = shared_mem_team.value

        ''' In production code we would be getting data from URL
            and would be sending the data via Queues         
        '''

        # if there is not a game coming anytime soon,
        # we want to slee for a longer time
        seconds_to_sleep = 10
        if parsed_pre_game_data['gameId'] is None:
            seconds_to_sleep = 86400

        # The final gameState data will only be donwloaded once
        # Also make sure there is a next gameId
        if (game_state != "Final" or parsed_pre_game_data['gameId'] is not None):
            live_game_data = nhlgamedata.fetch_live_game_data(parsed_pre_game_data['gameId'])
            parsed_live_game_data = nhlgamedata.get_parsed_live_game_data(live_game_data)

            ''' We need abbrevations from live data for our pre game data
            '''
            parsed_pre_game_data['awayTeam'] = parsed_live_game_data['awayTeam']
            parsed_pre_game_data['homeTeam'] = parsed_live_game_data['homeTeam']

            ''' We need to add current_team_id to pre_game and live_game
                data so that our color can be chosen based on what the user
                chose for which team, that is which team number the rest api received
            '''
            parsed_pre_game_data['currentTeamId'] = current_team_id
            parsed_live_game_data['currentTeamId'] = current_team_id

            ''' Check if the game is live or not
                Depending on the game state, tell the board to disply different things
            '''
            game_state = parsed_live_game_data['gameState']
            print(game_state)
            if (game_state == "Preview"):
                # now both pre and live have gameState
                parsed_pre_game_data['gameState'] = "Preview"
                rest_api_queue.put(parsed_pre_game_data)
                seconds_to_sleep = 60
                print('is preview')
            elif (game_state == "Live"):
                rest_api_queue.put(parsed_live_game_data)
                print('is live')
            # would never hit this becuase game_state != "Final"
            #elif (game_state == "Final"):
            #    rest_api_queue.put(parsed_live_game_data)
            #    print('is final')
            else:
                print('not any of those')
            # We will modifly the Previe and FInal if statemtns based on this extra info
            #elif (if the game has ended more than 15 minutes ago shut off the board)
            #elif (if the game is going to start in 15 minutes or less then turn on the board)
        else:
            if 'endTime' in parsed_live_game_data:
                game_end_time = time.mktime(parsed_live_game_data['endTime'].timetuple())

        # 10 second sleep function
        timeout = time.time() + seconds_to_sleep
        while True:
            # While we are sleeping check ever 0.25 seconds 
            # if the API updated the team id
            if current_team_id != shared_mem_team.value:
                break
            else:
                # if it's been 10 seconds break
                if time.time() > timeout:
                    break
                else:
                    time.sleep(0.25)


# this makes the flask app run
app = Flask(__name__)

# Queue for the REST API to send infomration to the Board process
rest_api_queue = Queue()

# Get the user settings 
settings = get_settings()

# At runtime set the team id to what was stored in settings
shared_memory_team_id = Value('i', settings['team_id'])

# Shared memory for example data to show things are updating 
#shared_memory_data = Array('c', str.encode('{"t": 0, "m": 0}'))

# Create the process for getting data in a loop
nhl_data_process = Process(target=set_team_and_fetch_nhl_data, args=(shared_memory_team_id,rest_api_queue,))
nhl_data_process.start()

# Create the process for running the board
board_process = Process(target=board, args=(rest_api_queue,))
board_process.start()

@app.route('/team/<int:team_id>', methods=['POST'])
def update_team(team_id):
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    ''' Todo
        use https://statsapi.web.nhl.com/api/v1/teams
        to pull down all the valid team ids
        so do this at startup of the program. maybe store it in a file.
        actaully you could use a shared memory array, i think 
    '''
    # THe lock was causing hangs when switching to a live game
    with shared_memory_team_id.get_lock():
        shared_memory_team_id.value = team_id
    rtn = json.dumps({'team': shared_memory_team_id.value},  separators=(',',':'))
    return rtn

@app.route('/team', methods=['GET'])
def show_team():
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    return str(shared_memory_team_id.value)

app.run(host='0.0.0.0')
