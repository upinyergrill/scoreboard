from rgbmatrix import graphics

def preview(matrix, font, color, game_data):
    graphics.DrawText(matrix, font, 48, 7, color, game_data['homeWin'])
