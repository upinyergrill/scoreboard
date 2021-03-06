from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from scrollable_text import ScrollableText
from matrix_carousel import MatrixCarousel
import time

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
    w = w - 1
    h = h - 1
    for i in range(y-h, y):
        graphics.DrawLine(matrix, x, i, x+w, i, graphics.Color(0, 0, 0))
        #graphics.DrawLine(matrix, x, i, x+w, i, graphics.Color(207, 10, 44))

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
    graphics.DrawText(matrix, font, 5, 7, color, str(game_data['awayTeam']))

def draw_home_team_abbr(matrix, font, color, game_data):
    clear_area(matrix, 48, 7, 12, 6)
    # Team Abbrevaitions position
    graphics.DrawText(matrix, font, 48, 7, color, str(game_data['homeTeam']))

def draw_away_team_score(matrix, font, color, game_data):
    clear_area(matrix, 20, 7, 8, 6)
    # Score positions
    graphics.DrawText(matrix, font, 20, 7, color, "{0:0=2d}".format(game_data['awayScore']))

def draw_home_team_score(matrix, font, color, game_data):
    clear_area(matrix, 36, 7, 8, 6)
    # Score positions
    graphics.DrawText(matrix, font, 36, 7, color, "{0:0=2d}".format(game_data['homeScore']))

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

def draw_carousel(matrix, font, color, game_data, seconds_to_sleep, break_loop):
    functions = [draw_carousel_sog,
             draw_carousel_hits,
             draw_carousel_blocked,
             draw_carousel_takeaway,
             draw_carousel_giveaway,
             draw_carousel_powerplay]
    args = [matrix, font, color, game_data]
    carousel = MatrixCarousel(functions, args, seconds_to_sleep, break_loop)
    carousel.run()

def draw_carousel_sog(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 15, 31, color, "{0:0=2d}".format(game_data['awaySog']))
    graphics.DrawText(matrix, font, 26, 31, color, "SoG")
    graphics.DrawText(matrix, font, 41, 31, color, "{0:0=2d}".format(game_data['homeSog']))
    
def draw_carousel_hits(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 13, 31, color, "{0:0=2d}".format(game_data['awayHits']))
    graphics.DrawText(matrix, font, 24, 31, color, "HITS")
    graphics.DrawText(matrix, font, 43, 31, color, "{0:0=2d}".format(game_data['homeHits']))

def draw_carousel_blocked(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 7, 31, color, "{0:0=2d}".format(game_data['awayBlocked']))
    graphics.DrawText(matrix, font, 18, 31, color, "BLOCKED")
    graphics.DrawText(matrix, font, 49, 31, color, "{0:0=2d}".format(game_data['homeBlocked']))

def draw_carousel_faceoff(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 7, 31, color, str(game_data['awayFoWins']))
    graphics.DrawText(matrix, font, 26, 31, color, "FO%")
    graphics.DrawText(matrix, font, 41, 31, color, str(game_data['homeFoWins']))

def draw_carousel_takeaway(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 4, 31, color, "{0:0=2d}".format(game_data['awayTakeaways']))
    graphics.DrawText(matrix, font, 15, 31, color, "TAKEAWAYS")
    graphics.DrawText(matrix, font, 54, 31, color, "{0:0=2d}".format(game_data['homeTakeaways']))

def draw_carousel_giveaway(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 4, 31, color, "{0:0=2d}".format(game_data['awayGiveaways']))
    graphics.DrawText(matrix, font, 15, 31, color, "GIVEAWAYS")
    graphics.DrawText(matrix, font, 54, 31, color, "{0:0=2d}".format(game_data['homeGiveaways']))

def draw_carousel_powerplay(matrix, font, color, game_data):
    clear_area(matrix, 1, 31, 61, 6)
    graphics.DrawText(matrix, font, 4, 31, color, str(game_data['awayPowerPlayStat']))
    graphics.DrawText(matrix, font, 19, 31, color, "PWRPLAY")
    graphics.DrawText(matrix, font, 50, 31, color, str(game_data['homePowerPlayStat']))
