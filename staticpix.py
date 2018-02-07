from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
import nhlgameinfo
import sys
import time
import requests
import datetime
import json

now = datetime.datetime.now()
date = now.strftime("%Y-%m-%d")

teamId = '14'
games = requests.get('https://statsapi.web.nhl.com/api/v1/teams/' +
                     teamId + '?expand=team.schedule.next&expand=team.schedule.previous')
parsed_games = (games.json())

nextgamedate = (parsed_games['teams'][0]
                ['nextGameSchedule']['dates'][0]['date'])
if date == nextgamedate:
    gamePK = (parsed_games['teams'][0]['nextGameSchedule']
              ['dates'][0]['games'][0]['gamePk'])
else:
    gamePK = (parsed_games['teams'][0]['previousGameSchedule']
              ['dates'][0]['games'][0]['gamePk'])

gameinfo = requests.get(
    'https://statsapi.web.nhl.com/api/v1/game/' + str(gamePK) + '/feed/live')
parsed_gameinfo = (gameinfo.json())

# RGBMatrix Options
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.brightness = 20

matrix = RGBMatrix(options=options)
font = graphics.Font()
font.LoadFont('Assets/tom-thumb.bdf')
color = graphics.Color(255, 255, 255)
color_off = graphics.Color(0, 0, 0)

# Draw lines to contain time and period info
for y in range(8, 23):
    matrix.SetPixel(20, y, 255, 235, 59)
for y in range(8, 23):
    matrix.SetPixel(42, y, 255, 235, 59)

for x in range(21, 42):
    matrix.SetPixel(x, 8, 255, 235, 59)
for x in range(21, 42):
    matrix.SetPixel(x, 22, 255, 235, 59)

for y in range(1, 8):
    matrix.SetPixel(31, y, 255, 235, 59)

# Scoreboard border
for y in range(0, 32):
    matrix.SetPixel(0, y, 255, 235, 59)
for y in range(0, 32):
    matrix.SetPixel(63, y, 255, 235, 59)

for x in range(0, 64):
    matrix.SetPixel(x, 0, 255, 235, 59)
for x in range(0, 64):
    matrix.SetPixel(x, 31, 255, 235, 59)

try:
    print("Press CTRL+C to stop.")
    while True:
        time_left = str(nhlgameinfo.timeLeft())
        period = str(nhlgameinfo.period())
        away_team = str(nhlgameinfo.awayTeam())
        home_team = str(nhlgameinfo.homeTeam())
        away_score = str(nhlgameinfo.awayScore())
        home_score = str(nhlgameinfo.homeScore())
        away_sog = str(nhlgameinfo.awaySog())
        home_sog = str(nhlgameinfo.homeSog())
        if time_left == "Final":
            time_left = "00:00"

        # with open('score.txt', 'r') as f:
        #     first_line = f.read()
        # Score positions
        graphics.DrawText(matrix, font, 36, 7, color_off, "88")
        graphics.DrawText(matrix, font, 36, 7, color_off, "11")
        graphics.DrawText(matrix, font, 36, 7, color, away_score)
        graphics.DrawText(matrix, font, 20, 7, color_off, "88")
        graphics.DrawText(matrix, font, 20, 7, color_off, "11")
        graphics.DrawText(matrix, font, 20, 7, color, home_score)

        # Shot on Goal positions
        graphics.DrawText(matrix, font, 41, 30, color_off, "88")
        graphics.DrawText(matrix, font, 41, 30, color_off, "11")
        graphics.DrawText(matrix, font, 41, 30, color, away_sog)
        graphics.DrawText(matrix, font, 15, 30, color_off, "88")
        graphics.DrawText(matrix, font, 15, 30, color_off, "11")
        graphics.DrawText(matrix, font, 15, 30, color, home_sog)

        # Team Abbrevaitions position
        graphics.DrawText(matrix, font, 48, 7, color, away_team)
        graphics.DrawText(matrix, font, 5, 7, color, home_team)

        # Time and Period positions
        graphics.DrawText(matrix, font, 22, 15, color_off, "88:88")
        graphics.DrawText(matrix, font, 22, 15, color_off, "11:11")
        graphics.DrawText(matrix, font, 22, 15, color, time_left)
        graphics.DrawText(matrix, font, 26, 21, color_off, "888")
        graphics.DrawText(matrix, font, 26, 21, color_off, "111")
        graphics.DrawText(matrix, font, 26, 21, color, period)
        graphics.DrawText(matrix, font, 26, 30, color, "SoG")

        # Penalty / Box Positions
        graphics.DrawText(matrix, font, 48, 15, color, "Box")
        graphics.DrawText(matrix, font, 5, 15, color, "Box")
        graphics.DrawText(matrix, font, 50, 20, color, "+")
        graphics.DrawText(matrix, font, 54, 20, color, "+")
        graphics.DrawText(matrix, font, 7, 20, color, "+")
        graphics.DrawText(matrix, font, 11, 20, color, "+")
        time.sleep(30)
        print("Cycling game info...")
except KeyboardInterrupt:
    sys.exit(0)