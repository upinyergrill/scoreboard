import requests
import json

def fetch_teams():
    '''fetches scheduled game info (gamepk number and team records)
    NOTE: team_id is an INT
    '''
    data = requests.get('https://statsapi.web.nhl.com/api/v1/teams/')
    teams = data.json()
    return teams['teams']

def format_teams(teams):
    formatted_teams = []
    for team in [d for d in teams if d['active'] == True]:
        formatted_teams.append({
            'id': team['id'],
            'name': team['name'],
            'abbreviation': team['abbreviation']
        })
    return formatted_teams

def get():
    return format_teams(fetch_teams())
