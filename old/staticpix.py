from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
import nhlgameinfo
import sys
import time
import requests
import datetime
import json
import importlib
from scroll_text import ScrollableText

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
team_color = json.load(open('Assets/nhlcolors.json'))
color = graphics.Color(255, 255, 255)
color_off = graphics.Color(0, 0, 0)

def borders():

    # Draw lines to contain time and period info
    for y in range(8, 23):
        matrix.SetPixel(20, y, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])
    for y in range(8, 23):
        matrix.SetPixel(42, y, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])

    for x in range(21, 42):
        matrix.SetPixel(x, 8, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])
    for x in range(21, 42):
        matrix.SetPixel(x, 22, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])

    for y in range(1, 8):
        matrix.SetPixel(31, y, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])

    # Scoreboard border
    for y in range(0, 32):
        matrix.SetPixel(0, y, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])
    for y in range(0, 32):
        matrix.SetPixel(63, y, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])

    for x in range(0, 64):
        matrix.SetPixel(x, 0, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])
    for x in range(0, 64):
        matrix.SetPixel(x, 31, team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b'])

# Penalty Box Boarder?
#for y in range(8, 21):
#    matrix.SetPixel(2, y, 255, 235, 59)
#for y in range(8, 21):
#    matrix.SetPixel(18, y, 255, 235, 59)
#
#for x in range(2, 18):
#    matrix.SetPixel(x, 8, 255, 235, 59)
#for x in range(2, 18):
#    matrix.SetPixel(x, 20, 255, 235, 59)
def clearInfo():
    graphics.DrawLine(matrix, 1, 24, 62, 24, color_off)
    graphics.DrawLine(matrix, 1, 25, 62, 25, color_off)
    graphics.DrawLine(matrix, 1, 26, 62, 26, color_off)
    graphics.DrawLine(matrix, 1, 27, 62, 27, color_off)
    graphics.DrawLine(matrix, 1, 28, 62, 28, color_off)
    graphics.DrawLine(matrix, 1, 29, 62, 29, color_off)
    graphics.DrawLine(matrix, 1, 30, 62, 30, color_off)

def SoG():
    away_sog = str(nhlgameinfo.awaySog())
    home_sog = str(nhlgameinfo.homeSog())
    clearInfo()
    graphics.DrawText(matrix, font, 26, 30, color, "SoG")
    graphics.DrawText(matrix, font, 41, 30, color, home_sog)
    graphics.DrawText(matrix, font, 15, 30, color, away_sog)

def hits():
    away_hits = str(nhlgameinfo.awayHits())
    home_hits = str(nhlgameinfo.homeHits())
    clearInfo()
    graphics.DrawText(matrix, font, 24, 30, color, "HITS")
    graphics.DrawText(matrix, font, 43, 30, color, home_hits)
    graphics.DrawText(matrix, font, 13, 30, color, away_hits)

def blocked():
    away_blocked = str(nhlgameinfo.awayBlocks())
    home_blocked = str(nhlgameinfo.homeBlocks())
    clearInfo()
    graphics.DrawText(matrix, font, 18, 30, color, "BLOCKED")
    graphics.DrawText(matrix, font, 49, 30, color, home_blocked)
    graphics.DrawText(matrix, font, 7, 30, color, away_blocked)

def faceoff():
    away_FOWins = str(nhlgameinfo.awayFOWins())
    home_FOWins = str(nhlgameinfo.homeFOWins())
    clearInfo()
    graphics.DrawText(matrix, font, 26, 30, color, "FO%")
    graphics.DrawText(matrix, font, 41, 30, color, home_FOWins)
    graphics.DrawText(matrix, font, 7, 30, color, away_FOWins)

def takeaway():
    away_takeaway = str(nhlgameinfo.awayTakeaways())
    home_takeaway = str(nhlgameinfo.homeTakeaways())
    clearInfo()
    graphics.DrawText(matrix, font, 14, 30, color, "TAKEAWAYS")
    graphics.DrawText(matrix, font, 53, 30, color, home_takeaway)
    graphics.DrawText(matrix, font, 3, 30, color, away_takeaway)

def giveaway():
    away_giveaway = str(nhlgameinfo.awayGiveaways())
    home_giveaway = str(nhlgameinfo.homeGiveaways())
    clearInfo()
    graphics.DrawText(matrix, font, 14, 30, color, "GIVEAWAYS")
    graphics.DrawText(matrix, font, 53, 30, color, home_giveaway)
    graphics.DrawText(matrix, font, 3, 30, color, away_giveaway)

def powerplay():
    away_pp = str(nhlgameinfo.awayPP())
    home_pp = str(nhlgameinfo.homePP())
    clearInfo()
    graphics.DrawText(matrix, font, 18, 30, color, "PWRPLAY")
    graphics.DrawText(matrix, font, 49, 30, color, home_pp)
    graphics.DrawText(matrix, font, 3, 30, color, away_pp)

try:
    print("Press CTRL+C to stop.")
    while True:
        importlib.reload(nhlgameinfo)
        matrix.Clear()
        borders()
        game_status = str(nhlgameinfo.gameStatus())
        if game_status != "Live":
        #if game_status != "Final":
            away_team = str(nhlgameinfo.awayTeam())
            away_win = "W-" + str(nhlgameinfo.awayWin()) + ""
            away_lose = "L-" + str(nhlgameinfo.awayLose()) + ""
            away_otl = "O-" + str(nhlgameinfo.awayOtl()) + ""
            home_team = str(nhlgameinfo.homeTeam())
            home_win = "W-" + str(nhlgameinfo.homeWin()) + ""
            home_lose = "L-" + str(nhlgameinfo.homeLose()) + ""
            home_otl = "O-" + str(nhlgameinfo.homeOtl()) + ""
            graphics.DrawText(matrix, font, 48, 7, color, home_team)
            graphics.DrawText(matrix, font, 46, 13, color, home_win)
            graphics.DrawText(matrix, font, 46, 19, color, home_lose)
            graphics.DrawText(matrix, font, 46, 25, color, home_otl)
            graphics.DrawText(matrix, font, 5, 7, color, away_team)
            graphics.DrawText(matrix, font, 3, 13, color, away_win)
            graphics.DrawText(matrix, font, 3, 19, color, away_lose)
            graphics.DrawText(matrix, font, 3, 25, color, away_otl)
            gametime = nhlgameinfo.gameTime()
            format_gametime = gametime.strftime('%a, %b %d, %I:%M%p')
            message = "NEXT GAME|" + format_gametime  + ""
            border_pixels = [[0, 30],[0, 29],[0, 28],[0, 27],[0, 26],[63, 30],[63, 29],[63, 28],[63, 27],[63, 26]]
            border_color = [team_color[nhlgameinfo.teamID()]['r'], team_color[nhlgameinfo.teamID()]['g'], team_color[nhlgameinfo.teamID()]['b']]
            scroll_text = ScrollableText()
            scroll_text.scroll(matrix, font, 31, color, message, border_pixels, border_color)
            time.sleep(0.5)
            print("Cycling game info...")
        else:
            time_left = str(nhlgameinfo.timeLeft())
            period = str(nhlgameinfo.period())
            away_team = str(nhlgameinfo.awayTeam())
            home_team = str(nhlgameinfo.homeTeam())
            away_score = str(nhlgameinfo.awayScore())
            home_score = str(nhlgameinfo.homeScore())
            if time_left == "END":
                 period = "INT"
                 time_left = str(nhlgameinfo.intTime())

            # Score positions
            graphics.DrawText(matrix, font, 36, 7, color, home_score)
            graphics.DrawText(matrix, font, 20, 7, color, away_score)

            # Shot on Goal positions
            #graphics.DrawText(matrix, font, 41, 30, color, home_sog)
            #graphics.DrawText(matrix, font, 15, 30, color, away_sog)

            # Team Abbrevaitions position
            graphics.DrawText(matrix, font, 47, 7, color, home_team)
            graphics.DrawText(matrix, font, 5, 7, color, away_team)

            # Time and Period positions
            graphics.DrawText(matrix, font, 22, 15, color, time_left)
            graphics.DrawText(matrix, font, 26, 21, color, period)
            #graphics.DrawText(matrix, font, 26, 30, color, "SoG")

            # Penalty / Box Positions
            # Need to check if powerplay is true if it is 4v4 or if that counts a False
            if (nhlgameinfo.homeSkaters() == 4) and (nhlgameinfo.awayPowerPlay() == True):
                graphics.DrawText(matrix, font, 47, 15, color, "Box")
                graphics.DrawText(matrix, font, 49, 20, color, "+")
            if (nhlgameinfo.homeSkaters() == 3) and (nhlgameinfo.awayPowerPlay() == True):
                graphics.DrawText(matrix, font, 47, 15, color, "Box")
                graphics.DrawText(matrix, font, 49, 20, color, "+")
                graphics.DrawText(matrix, font, 53, 20, color, "+")
            if (nhlgameinfo.awaySkaters() == 4) and (nhlgameinfo.homePowerPlay() == True):
                graphics.DrawText(matrix, font, 5, 15, color, "Box")
                graphics.DrawText(matrix, font, 7, 20, color, "+")
            if (nhlgameinfo.awaySkaters() == 3) and (nhlgameinfo.homePowerPlay() == True):
                graphics.DrawText(matrix, font, 5, 15, color, "Box")
                graphics.DrawText(matrix, font, 7, 20, color, "+")
                graphics.DrawText(matrix, font, 11, 20, color, "+")
            if (nhlgameinfo.awaySkaters() == 4) and (nhlgameinfo.homeSkaters() == 4):
                graphics.DrawText(matrix, font, 47, 15, color, "Box")
                graphics.DrawText(matrix, font, 49, 20, color, "+")
                graphics.DrawText(matrix, font, 5, 15, color, "Box")
                graphics.DrawText(matrix, font, 7, 20, color, "+")
            SoG()
            time.sleep(2)
            hits()
            time.sleep(2)
            blocked()
            time.sleep(2)
            faceoff()
            time.sleep(2)
            takeaway()
            time.sleep(2)
            giveaway()
            time.sleep(2)
            powerplay()
            time.sleep(3)
            print("Cycling game info...")
except KeyboardInterrupt:
    sys.exit(0)
