''' 1. first had to install flask
    pip3 install flask
    2. then had to add this file to my exports
    export FLASK_APP=flask_example.py
    3. then i ran flask
    python3 -m flask run
'''
from flask import Flask
from multiprocessing import Process, Value, Array
from rpyc.utils.server import ThreadedServer
import rpyc
import time

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/team/<int:team_id>')
def show_team(team_id):
    conn = rpyc.connect("localhost", 40919)
    c = conn.root
    return 'User %d' % c.testthings(team_id)

class MyService(rpyc.Service):
    # this doesnt work either
    ''' def __init__(self, needed_a_second_param):
        self.smi = Value('i', 0) '''

    def exposed_testthings(self, x):
        # sucks the scope is mixed but idk what else to do
        shared_memory_int.value = shared_memory_int.value + x
        return shared_memory_int.value

# Shared memory value
shared_memory_int = Value('i', 0)

# start the rpyc server
server = ThreadedServer(MyService, port = 40919)
c = Process(target=server.start)
c.start()

