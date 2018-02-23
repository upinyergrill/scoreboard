''' 1. first had to install flask
    pip3 install flask
    2. then had to add this file to my exports
    export FLASK_APP=flask_example.py
    3. then i ran flask
    python3 -m flask run
'''
from flask import Flask
from multiprocessing import Value, Process, Queue, Array
import json
import time

def fetch_nhl_data(shared_mem_team, shared_mem_data):
    while True:
        current_team_id = shared_mem_team.value
        millis = str(int(round(time.time())))[-2:]
        json_string = '{"t": ' + str(current_team_id) + ',"m":' + millis + '}'
        with shared_mem_data.get_lock():
            shared_mem_data.value = str.encode(json_string)
        timeout = time.time() + 10
        while True:
            if current_team_id != shared_mem_team.value:
                break
            else:
                if time.time() > timeout:
                    break
                else:
                    time.sleep(0.25)

app = Flask(__name__)

# Shared memory value 
shared_memory_team_id = Value('i', 0)
#shared_memory_data = Value('i', 0)
shared_memory_data = Array('c', str.encode('{"team": 0, "time": 0}'))

nhl_data_process = Process(target=fetch_nhl_data, args=(shared_memory_team_id,shared_memory_data,))
nhl_data_process.start()

@app.route('/team/<int:team_id>', methods=['GET', 'POST'])
def update_team(team_id):
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    with shared_memory_team_id.get_lock():
        shared_memory_team_id.value = team_id
    rtn = json.dumps({'team': shared_memory_team_id.value},  separators=(',',':'))
    return rtn

@app.route('/team', methods=['GET', 'POST'])
def show_team():
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    #rtn = json.dumps({'data': shared_memory_data.value},  separators=(',',':'))
    #return rtn
    return shared_memory_data.value.decode()
