''' 1. first had to install flask
    pip3 install flask
    2. then had to add this file to my exports
    export FLASK_APP=flask_example.py
    3. then i ran flask
    python3 -m flask run
'''
from flask import Flask

app = Flask(__name__)

@app.route('/')
def index():
    return 'Index Page'

@app.route('/hello')
def hello():
    return 'Hello, World'

@app.route('/user/<username>')
def show_user_profile(username):
    # show the user profile for that user
    return 'User %s' % username

@app.route('/post/<int:post_id>')
def show_post(post_id):
    # show the post with the given id, the id is an integer
    return 'Post %d' % post_id

@app.route('/team/<team_id>')
def show_team(team_id):
    # show the user profile for that user
    return 'Team %s' % team_id
