from rgbmatrix import graphics

def preview(matrix, font, color, game_data):
    clear_area(matrix, 6, 6, 5, 5)
    graphics.DrawText(matrix, font, 6, 6, color, str(game_data['homeTeam']))

def clear_area(matrix, x, y, w, h):
    '''Make this so it doesn't overwite borders on accident, maths
    '''
    for i in range(y-h, y):
        graphics.DrawLine(matrix, x, i, x+w, i, graphics.Color(0, 0, 0))

def draw_time_period_border(matrix, font, color):
    # Draw lines to contain time and period info
    for y in range(8, 23):
        matrix.SetPixel(20, y, color)
    for y in range(8, 23):
        matrix.SetPixel(42, y, color)

    for x in range(21, 42):
        matrix.SetPixel(x, 8, color)
    for x in range(21, 42):
        matrix.SetPixel(x, 22, color)

    for y in range(1, 8):
        matrix.SetPixel(31, y, color)

def draw_outer_border(matrix, font, color):
    # Scoreboard border
    for y in range(0, 32):
        matrix.SetPixel(0, y, color)
    for y in range(0, 32):
        matrix.SetPixel(63, y, color)

    for x in range(0, 64):
        matrix.SetPixel(x, 0, color)
    for x in range(0, 64):
        matrix.SetPixel(x, 31, color)
