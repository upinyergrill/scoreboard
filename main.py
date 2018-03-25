''' Execution Instructions
    su
    export FLASK_APP=main.py
    python3 -m flask run
'''
from rgbmatrix import graphics
from multiprocessing import Value, Process, Queue
from threading import Thread
from flask import Flask
from flask import Response
import json
import nhl_teams as nhlteams
import view
import controller


# Get the user settings 
settings = json.load(open('settings.json'))

# Get list of teams
active_nhl_teams = nhlteams.get()

# Set font
font = graphics.Font()
font.LoadFont('Assets/tom-thumb.bdf')

# load team colors
team_colors = json.load(open('Assets/nhlcolors.json'))

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
nhl_data_process = Process(target=controller.set_team_and_fetch_nhl_data, args=(shared_memory_team_id,rest_api_queue,shared_memory_board_state,shared_memory_board_brightness,shared_memory_sleep_timer,))

# Create the process for running the board
board_process = Process(target=view.board, args=(rest_api_queue,shared_memory_board_state,shared_memory_board_brightness,font,team_colors,))

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
    
    res = json.dumps({'brightness': shared_memory_board_brightness.value},  separators=(',',':'))
    return Response(res, status=200, mimetype='application/json')

app.run(host='0.0.0.0')
