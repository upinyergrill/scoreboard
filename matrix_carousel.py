import time
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


class MatrixCarousel(object):
    def __init__(self, functions, args, seconds_to_sleep, break_loop):
        object.__init__(self)
        self.functions = functions
        self.args = args
        self.seconds_to_sleep = seconds_to_sleep
        self.break_loop = break_loop

    def run(self):        
        while bool(self.break_loop.value) is False:
            for function in self.functions:
                function(self.args[0], self.args[1], self.args[2], self.args[3])
                timeout = time.time() + self.seconds_to_sleep
                while bool(self.break_loop.value) is False:
                    if time.time() > timeout:
                        break
                    else:
                        time.sleep(0.1)
                # need this if statement to make it break from the for loop
                if bool(self.break_loop.value) is True:
                    break
