from threading import Thread
import nhl_board_render as nhlboardrender

class ScrollNextGameThread (Thread):
    def __init__(self, matrix, font, text_color, border_color, game_data, break_loop):
        Thread.__init__(self)
        self.matrix = matrix
        self.font = font
        self.text_color = text_color
        self.border_color = border_color
        self.game_data = game_data
        self.break_loop = break_loop

    def run(self):
        # By default self.name is Thread-N
        print("Starting " + self.name)
        nhlboardrender.draw_scrolling_next_game(self.matrix, self.font, self.text_color, self.border_color, self.game_data, self.break_loop)
        print("Exiting " + self.name)
