''' 1. first had to install flask
    pip3 install flask
    2. then had to add this file to my exports
    export FLASK_APP=flask_example.py
    3. then i ran flask
    python3 -m flask run
'''
from flask import Flask
from multiprocessing import  Value

app = Flask(__name__)

# Shared memory value
shared_memory_int = Value('i', 0)

@app.route('/team/<int:team_id>', methods=['GET', 'POST'])
def show_team(team_id):
    # sucks that i'm violating scope 
    # but I can't figure out how to make it a param
    shared_memory_int.value = shared_memory_int.value + team_id
    return 'User %d' % shared_memory_int.value
