''' Execution Instructions
    su
    export FLASK_APP=flask_example.py
    python3 -m flash run
'''
from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from multiprocessing import Value, Process, Queue, Array
from flask import Flask
from flask import Response
import json
import time
import nhl_game_data as nhlgamedata
import nhl_board_render as nhlboardrender
from datetime import datetime
import nhl_teams as nhlteams

def get_time_since_game_ended(seconds):
    return time.time() - seconds

# The Board
def board(rest_api_queue, shared_board_state, shared_board_brightness):
    ''' The main function of the Board process should be waiting
        for the REST API process to send it data
        
        The process should also handle starting and stopping
        all the other sub processes for 
        getting and display data on the board '''
    # Create the process for running the board
    #rest_api_queue = Queue()
    #board_process = Process(target=board, args=(rest_api_queue,))
    #board_process.start()

    # Things that wont change on board
    font = graphics.Font()
    font.LoadFont('Assets/tom-thumb.bdf')
    team_colors = json.load(open('Assets/nhlcolors.json'))
    color_white = graphics.Color(255, 255, 255)

    while True:
        # init board state
        current_board_state = shared_board_state.value
        # Init brightness from shared mem
        current_brightness = shared_board_brightness.value

        # RGBMatrix Options
        options = RGBMatrixOptions()
        options.rows = 32
        options.chain_length = 2
        options.brightness = current_brightness * 20
        options.gpio_slowdown = 2
        options.drop_privileges = 0

        # Create matrix with optiosn
        matrix = RGBMatrix(options = options)
        
        print('the board started')

        # Keep track of game state
        # this way we can clear the board to get ready for a new view
        current_game_state = None

        while True:
            try:
                game_data = rest_api_queue.get(False)
                
                # If brightness changes, re-render the board
                if (current_brightness != shared_board_brightness.value):
                    # TODO: I'm not sure if this will make the matrix __dealloc__
                    # or not but i saw in the source the class's __dealloc__ method
                    # has the Clear function in it, so it shoudl be easy to test
                    matrix = None
                    break
                
                
                current_brightness = shared_board_brightness.value

                print('board got game data')
                print(game_data)
                print('current_board_state', current_board_state)
                print('shared_board_state', shared_board_state.value)
                # Clear the board, but only clear if the state has changed from 1 to 0
                if (current_board_state == 1 and shared_board_state.value == 0):
                    matrix.Clear()
                elif (current_board_state == 0 and shared_board_state.value ==0):
                    # The board is off, leave it offs
                    pass
                else:
                    # Check if the game state has changed
                    # life cylce
                    # preview -> live   | Clear
                    # live -> final     | Don't clear
                    # final -> preview  | Clear
                    if (current_game_state is not None):
                        if (current_game_state == "Preview" and game_data['gameState'] == "Live"):
                            matrix.Clear()
                        elif (current_game_state == "Live" and game_data['gameState'] == "Final"):
                            pass
                        if (current_game_state == "Final" and game_data['gameState'] == "Preview"):
                            matrix.Clear()

                    current_game_state = game_data['gameState']

                    #print(team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
                    nhlboardrender.draw_outer_border(matrix, font, team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
                    nhlboardrender.draw_time_period_border(matrix, font, team_colors[str(game_data['currentTeamId'])]['r'], team_colors[str(game_data['currentTeamId'])]['g'], team_colors[str(game_data['currentTeamId'])]['b'])
                    
                    if (current_game_state == "Preview"):
                        print('should render')
                        nhlboardrender.draw_away_team_pre_game(matrix, font, color_white, game_data)
                        nhlboardrender.draw_home_team_pre_game(matrix, font, color_white, game_data)
                        print('is it blocking code?')
                        #pass
                    elif(current_game_state == "Live" or current_game_state == "Final"):
                        pass
                    pass
                
                # Update current board state for next iteration of loop
                # dont need this, setting in set_team_and_fetch_nhl_data
                current_board_state = shared_board_state.value
            except:
                pass

def set_team_and_fetch_nhl_data(shared_mem_team, rest_api_queue, shared_board_state, shared_board_brightness, shared_sleep_timer):
    # At runtime set the shared_mem_team value (the settings team id)
    # to the current team id 
    current_team_id = shared_mem_team.value
    # do the same for the board state
    # Update current board state for next iteration of loop
    current_board_state = shared_board_state.value
    # do this for the birghtness too
    current_brightness = shared_board_brightness.value
    # game state get set later by fetch and parse
    game_state = None
    game_end_time = None
    
    # Always get pregame data at boot
    pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
    parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)
    
    # Never break from outer loop
    while True:
        # Basically the point of all this code here is 
        # so we dont keep downloading the pre game data is the game is live
        
        # User changed to another team, start the process over
        if current_team_id != shared_mem_team.value:
            # get pre game data
            pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
            parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)

        # Store what the current team is for comparison
        current_team_id = shared_mem_team.value
        # do the same for the board state
        current_board_state = shared_board_state.value
        # do the same for the brightness
        current_brightness = shared_board_brightness.value

        # What happens here is if the game has been over for more than 15 minutes,
        # get the next game data, which will be in state "Preview" so if the game was 
        # showing live data this will make it show preview data for the next game
        if game_end_time is not None:
            if get_time_since_game_ended(game_end_time) > 900:
                # get pre game data
                pre_game_data = nhlgamedata.fetch_pre_game_data(shared_mem_team.value)
                parsed_pre_game_data = nhlgamedata.get_parsed_pre_game_data(pre_game_data)

        ''' If the game has been over for 15 minutes from now
            and the next game doesn't for more than 15 minutes from now
            shared_sleep_timer == 0 means don't turn off ever
        ''' 
        if shared_sleep_timer.value != 0:
            if game_end_time is not None:
                if get_time_since_game_ended(game_end_time) > shared_sleep_timer.value * 60:
                    with shared_board_state.get_lock():
                        shared_board_state.value = 0

            game_start_time = time.mktime(parsed_pre_game_data['gameStartDateTime'].timetuple())
            time_until_next_game_starts = game_start_time - time.time()
            if time_until_next_game_starts > shared_sleep_timer.value * 60:
                with shared_board_state.get_lock():
                    shared_board_state.value = 0

        # if there is not a game coming anytime soon,
        # we want to slee for a longer time
        seconds_to_sleep = 10
        if parsed_pre_game_data['gameId'] is None:
            seconds_to_sleep = 86400

        # The final gameState data will only be donwloaded once
        # Also make sure there is a next gameId
        # If game is Live or Preview
        #if (game_state != "Final" or parsed_pre_game_data['gameId'] is not None):
        if (parsed_pre_game_data['gameId'] is not None):
            # Download live data
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
            elif (game_state == "Final"):
                rest_api_queue.put(parsed_live_game_data)
                print('is final')
            else:
                print('not any of those')
            # We will modifly the Previe and FInal if statemtns based on this extra info
            #elif (if the game has ended more than 15 minutes ago shut off the board)
            #elif (if the game is going to start in 15 minutes or less then turn on the board)
        else:
            if 'gameEndDateTime' in parsed_live_game_data:
                game_end_time = time.mktime(parsed_live_game_data['gameEndDateTime'].timetuple())

        # 10 second sleep function
        timeout = time.time() + seconds_to_sleep
        while True:
            # While we are sleeping check ever 0.25 seconds 
            # if the API updated the team id
            if current_team_id != shared_mem_team.value:
                break
            elif current_board_state != shared_board_state.value:
                break
            elif current_brightness != shared_board_brightness.value:
                break
            else:
                # if it's been 10 seconds break
                if time.time() > timeout:
                    break
                else:
                    time.sleep(0.25)

# Get the user settings 
settings = json.load(open('settings.json'))

# Get list of teams
active_nhl_teams = nhlteams.get()

# We want to do application setup before this
# this makes the flask app run
app = Flask(__name__)

# Queue for the REST API to send infomration to the Board process
rest_api_queue = Queue()

# At runtime set the team id to what was stored in settings
shared_memory_team_id = Value('i', settings['team_id'])

# At runtime set the board to be on
shared_memory_board_state = Value('i', 1)

# At runtime set the board to automically turn off after a certain amout of time
shared_memory_sleep_timer = Value('i', settings['sleep_timer'])

# At runtime configure brightness
shared_memory_board_brightness = Value('i', settings['brightness'])

# Create the process for getting data in a loop
nhl_data_process = Process(target=set_team_and_fetch_nhl_data, args=(shared_memory_team_id,rest_api_queue,shared_memory_board_state,shared_memory_board_brightness,shared_memory_sleep_timer,))

# Create the process for running the board
board_process = Process(target=board, args=(rest_api_queue,shared_memory_board_state,shared_memory_board_brightness,))

# Start processes
nhl_data_process.start()
board_process.start()

@app.route('/team/<int:team_id>', methods=['GET'])
def update_team(team_id):
    # Make sure the team they specified is valid
    if (any(team['id'] == team_id for team in active_nhl_teams)):
        # sucks that i'm violating scope 
        # but I can't figure out how to make it a param
        # Bug Resolved - THe lock was causing hangs when switching to a live game
        with shared_memory_team_id.get_lock():
            shared_memory_team_id.value = team_id
        res = json.dumps({'team_id': shared_memory_team_id.value},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')
    else:
        return Response("{'error':'not a valid team id'}", status=422, mimetype='application/json')

@app.route('/team', methods=['GET'])
def show_team():
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    res = json.dumps({'team_id': shared_memory_team_id.value},  separators=(',',':'))
    return Response(res, status=200, mimetype='application/json')

@app.route('/team/default/<int:team_id>', methods=['GET'])
def change_default_team(team_id):
    # Make sure the team they specified is valid
    if (any(team['id'] == team_id for team in active_nhl_teams)):
        # TODO: make this update the setting.json file
        res = json.dumps({'team_id': team_id},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')
    else:
        return Response("{'error':'not a valid team id.  See /team/all for list.'}", status=422, mimetype='application/json')

@app.route('/team/default', methods=['GET'])
def get_default_team():
    settings = json.load(open('settings.json'))
    res = json.dumps({'team_id': settings['team_id']},  separators=(',',':'))
    return Response(res, status=200, mimetype='application/json')

@app.route('/team/all', methods=['GET'])
def return_all_teams():
    res = json.dumps(active_nhl_teams)
    return Response(res, status=200, mimetype='application/json')

@app.route('/board/state/<int:board_state>', methods=['GET'])
def change_board_state(board_state):
    board_off = 0
    board_on = 1
    if (board_state == board_off or board_state == board_on):
        with shared_memory_board_state.get_lock():
            shared_memory_board_state.value = board_state
        res = json.dumps({'state': board_state},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')
    else:
        return Response("{'error':'not a valid state. Choose 0-1. 0 is off.'}", status=422, mimetype='application/json')

@app.route('/board/state', methods=['GET'])
def get_board_state():
        res = json.dumps({'state': shared_memory_board_state.value},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')

@app.route('/board/timer/<int:sleep_timer>', methods=['GET'])
def change_board_timer(sleep_timer):
    if 0 <= sleep_timer <= 1440:
        # TODO: make this update the settings.json file
        with shared_memory_sleep_timer.get_lock():
            shared_memory_sleep_timer.value = sleep_timer
        res = json.dumps({'timer': sleep_timer},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')
    else:
        return Response("{'error':'not a valid time. Choose 0-1440.  0 is never.'}", status=422, mimetype='application/json')

@app.route('/board/timer', methods=['GET'])
def get_board_timer():
    settings = json.load(open('settings.json'))
    res = json.dumps({'timer': settings['sleep_timer']},  separators=(',',':'))
    return Response(res, status=200, mimetype='application/json')

@app.route('/board/brightness/<int:board_brightness>', methods=['GET'])
def change_board_brightness(board_brightness):
    if 1 <= board_brightness <= 4:
        # TODO: make this update the settings.json file
        with shared_memory_board_brightness.get_lock():
            shared_memory_board_brightness.value = board_brightness
        res = json.dumps({'brightness': board_brightness},  separators=(',',':'))
        return Response(res, status=200, mimetype='application/json')
    else:
        return Response("{'error':'not a valid brightness. Choose 1-4'}", status=422, mimetype='application/json')

@app.route('/board/brightness', methods=['GET'])
def get_board_brightness():
    settings = json.load(open('settings.json'))
    res = json.dumps({'brightness': settings['brightness']},  separators=(',',':'))
    return Response(res, status=200, mimetype='application/json')

app.run(host='0.0.0.0')
