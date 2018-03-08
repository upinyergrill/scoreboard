from rgbmatrix import graphics

def preview(matrix, font, color, game_data):
    clear_area(matrix, 6, 6, 10, 10)
    graphics.DrawText(matrix, font, 6, 6, color, str(game_data['homeTeam']))

def clear_area(matrix, x, y, w, h):
    for i in range(y, y+h): 
        graphics.DrawLine(matrix, x, i, x+w, i, graphics.Color(0, 0, 0))
