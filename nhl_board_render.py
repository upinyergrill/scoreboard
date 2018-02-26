from rgbmatrix import graphics

def preview(matrix, font, color, game_data):
    matrix.Clear()
    graphics.DrawText(matrix, font, 6, 6, color, str(game_data['homeTeam']))
