from rgbmatrix import graphics
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
    for i in range(y-h, y):
        graphics.DrawLine(matrix, x, i, x+w, i, graphics.Color(0, 0, 0))

def draw_time_period_border(matrix, font, r, g, b):
    # Draw lines to contain time and period info
    for y in range(8, 23):
        matrix.SetPixel(20, y, r, g, b)
    for y in range(8, 23):
        matrix.SetPixel(42, y, r, g, b)

    for x in range(21, 42):
        matrix.SetPixel(x, 8, r, g, b)
    for x in range(21, 42):
        matrix.SetPixel(x, 22, r, g, b)

    for y in range(1, 8):
        matrix.SetPixel(31, y, r, g, b)

def draw_outer_border(matrix, font, r, g, b):
    # Scoreboard border
    for y in range(0, 32):
        matrix.SetPixel(0, y, r, g, b)
    for y in range(0, 32):
        matrix.SetPixel(63, y, r, g, b)

    for x in range(0, 64):
        matrix.SetPixel(x, 0, r, g, b)
    for x in range(0, 64):
        matrix.SetPixel(x, 31, r, g, b)

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

def draw_scrolling_next_game(matrix, font, text_color, border_color, game_data, options):
    clear_area(matrix, 1, 30, 62, 6)
    message = "NEXT GAME|" + game_data['gameStartDateTimeFormatted']
    border_pixels = [[0, 30],[0, 29],[0, 28],[0, 27],[0, 26],[63, 30],[63, 29],[63, 28],[63, 27],[63, 26]]
    scroll_text = ScrollableText()
    scroll_text.scroll(matrix, font, 31, text_color, message, border_pixels, border_color)
