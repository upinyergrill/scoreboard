from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from scrollable_text import ScrollableText

def draw_away_team_pre_game(matrix, font, color, game_data):
    clear_area(matrix, 5, 7, 12, 6)
    clear_area(matrix, 3, 13, 15, 6)
    clear_area(matrix, 3, 19, 15, 6)
    clear_area(matrix, 3, 25, 15, 6)
    graphics.DrawText(matrix, font, 5, 7, color, str(game_data['awayTeam']))
    graphics.DrawText(matrix, font, 3, 13, color, "W-" + str(game_data['awayWin']))
    graphics.DrawText(matrix, font, 3, 19, color, "L-" + str(game_data['awayLoss']))
    graphics.DrawText(matrix, font, 3, 25, color, "O-" + str(game_data['awayOtl']))

def preview(matrix, font, color, game_data):
    clear_area(matrix, 6, 6, 5, 5)
    graphics.DrawText(matrix, font, 6, 6, color, str(game_data['homeTeam']))

def clear_area(matrix, x, y, w, h):
    '''Make this so it doesn't overwite borders on accident, maths
    '''
    width = w - 1
    for i in range(y-h, y):
        graphics.DrawLine(matrix, x, i, x+width, i, graphics.Color(255, 0, 0))

def draw_time_period_border(matrix, font, color):
    # Draw lines to contain time and period info
    for y in range(8, 23):
        matrix.SetPixel(20, y, color['r'], color['g'], color['b'])
    for y in range(8, 23):
        matrix.SetPixel(42, y, color['r'], color['g'], color['b'])

    for x in range(21, 42):
        matrix.SetPixel(x, 8, color['r'], color['g'], color['b'])
    for x in range(21, 42):
        matrix.SetPixel(x, 22, color['r'], color['g'], color['b'])

    for y in range(1, 8):
        matrix.SetPixel(31, y, color['r'], color['g'], color['b'])

def draw_outer_border(matrix, font, color):
    # Scoreboard border
    for y in range(0, 32):
        matrix.SetPixel(0, y, color['r'], color['g'], color['b'])
    for y in range(0, 32):
        matrix.SetPixel(63, y, color['r'], color['g'], color['b'])

    for x in range(0, 64):
        matrix.SetPixel(x, 0, color['r'], color['g'], color['b'])
    for x in range(0, 64):
        matrix.SetPixel(x, 31, color['r'], color['g'], color['b'])

def draw_home_team_pre_game(matrix, font, color, game_data):
    clear_area(matrix, 48, 7, 12, 6)
    clear_area(matrix, 46, 13, 15, 6)
    clear_area(matrix, 46, 19, 15, 6)
    clear_area(matrix, 46, 25, 15, 6)
    home_team = str(game_data['homeTeam'])
    home_win = "W-" + str(game_data['homeWin']) + ""
    home_lose = "L-" + str(game_data['homeLoss']) + ""
    home_otl = "O-" + str(game_data['homeOtl']) + ""
    graphics.DrawText(matrix, font, 48, 7, color, home_team)
    graphics.DrawText(matrix, font, 46, 13, color, home_win)
    graphics.DrawText(matrix, font, 46, 19, color, home_lose)
    graphics.DrawText(matrix, font, 46, 25, color, home_otl)

def draw_scrolling_next_game(matrix, font, text_color, border_color, game_data, break_loop):
    clear_area(matrix, 1, 31, 61, 6)
    message = "NEXT GAME|" + game_data['gameStartDateTimeFormatted']
    border_pixels = [[0, 30],[0, 29],[0, 28],[0, 27],[0, 26],[63, 30],[63, 29],[63, 28],[63, 27],[63, 26]]
    scroll_text = ScrollableText()
    scroll_text.scroll(matrix, font, 31, text_color, message, border_pixels, border_color, break_loop)

def draw_away_team_abbr(matrix, font, color, game_data):
    clear_area(matrix, 5, 7, 12, 6)
    # Score positions
    graphics.DrawText(matrix, font, 5, 7, color, str(game_data['homeTeam']))

def draw_home_team_abbr(matrix, font, color, game_data):
    clear_area(matrix, 47, 7, 12, 6)
    # Team Abbrevaitions position
    graphics.DrawText(matrix, font, 47, 7, color, str(game_data['homeTeam']))

def draw_away_team_score(matrix, font, color, game_data):
    clear_area(matrix, 20, 7, 8, 6)
    # Score positions
    graphics.DrawText(matrix, font, 20, 7, color, str(game_data['awayScore']))

def draw_home_team_score(matrix, font, color, game_data):
    clear_area(matrix, 36, 7, 8, 6)
    # Score positions
    graphics.DrawText(matrix, font, 36, 7, color, str(game_data['homeScore']))

def draw_period(matrix, font, color, game_data):
    clear_area(matrix, 26, 21, 12, 6)
    # TODO look more into whati should do about this 
    # There is a change currentPeriodOrdinal will not exist 
    graphics.DrawText(matrix, font, 26, 21, color, str(game_data['currentPeriodOrdinal']))

def draw_live_helper(matrix, font, color, game_data):
    draw_home_team_abbr(matrix, font, color, game_data)
    draw_away_team_abbr(matrix, font, color, game_data)
    draw_home_team_score(matrix, font, color, game_data)
    draw_away_team_score(matrix, font, color, game_data)
    draw_period(matrix, font, color, game_data)

''' def draw_carousel_sog(matrix, font, color, game_data):
    away_sog = str(nhlgameinfo.awaySog())
    home_sog = str(nhlgameinfo.homeSog())
    clearInfo()
    graphics.DrawText(matrix, font, 26, 30, color, "SoG")
    graphics.DrawText(matrix, font, 41, 30, color, home_sog)
    graphics.DrawText(matrix, font, 15, 30, color, away_sog)

def draw_carousel_hits(matrix, font, color, game_data):
    away_hits = str(nhlgameinfo.awayHits())
    home_hits = str(nhlgameinfo.homeHits())
    clearInfo()
    graphics.DrawText(matrix, font, 24, 30, color, "HITS")
    graphics.DrawText(matrix, font, 43, 30, color, home_hits)
    graphics.DrawText(matrix, font, 13, 30, color, away_hits)

def draw_carousel_blocked(matrix, font, color, game_data):
    away_blocked = str(nhlgameinfo.awayBlocks())
    home_blocked = str(nhlgameinfo.homeBlocks())
    clearInfo()
    graphics.DrawText(matrix, font, 18, 30, color, "BLOCKED")
    graphics.DrawText(matrix, font, 49, 30, color, home_blocked)
    graphics.DrawText(matrix, font, 7, 30, color, away_blocked)

def draw_carousel_faceoff(matrix, font, color, game_data):
    away_FOWins = str(nhlgameinfo.awayFOWins())
    home_FOWins = str(nhlgameinfo.homeFOWins())
    clearInfo()
    graphics.DrawText(matrix, font, 26, 30, color, "FO%")
    graphics.DrawText(matrix, font, 41, 30, color, home_FOWins)
    graphics.DrawText(matrix, font, 7, 30, color, away_FOWins)

def draw_carousel_takeaway(matrix, font, color, game_data):
    away_takeaway = str(nhlgameinfo.awayTakeaways())
    home_takeaway = str(nhlgameinfo.homeTakeaways())
    clearInfo()
    graphics.DrawText(matrix, font, 14, 30, color, "TAKEAWAYS")
    graphics.DrawText(matrix, font, 53, 30, color, home_takeaway)
    graphics.DrawText(matrix, font, 3, 30, color, away_takeaway)

def draw_carousel_giveaway(matrix, font, color, game_data):
    away_giveaway = str(nhlgameinfo.awayGiveaways())
    home_giveaway = str(nhlgameinfo.homeGiveaways())
    clearInfo()
    graphics.DrawText(matrix, font, 14, 30, color, "GIVEAWAYS")
    graphics.DrawText(matrix, font, 53, 30, color, home_giveaway)
    graphics.DrawText(matrix, font, 3, 30, color, away_giveaway)

def draw_carousel_powerplay(matrix, font, color, game_data):
    away_pp = str(nhlgameinfo.awayPP())
    home_pp = str(nhlgameinfo.homePP())
    clearInfo()
    graphics.DrawText(matrix, font, 18, 30, color, "PWRPLAY")
    graphics.DrawText(matrix, font, 49, 30, color, home_pp)
    graphics.DrawText(matrix, font, 3, 30, color, away_pp)
 '''