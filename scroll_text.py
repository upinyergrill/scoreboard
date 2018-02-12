import time
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


class ScrollableText(object):
    def __init__(self, options=None):
        if options:
            if not isinstance(options, RGBMatrixOptions):
                raise ValueError('options must be type RGBMatrixOptions')
        else:
            # RGBMatrix Options
            options = RGBMatrixOptions()
            options.rows = 32
            options.chain_length = 2
            options.brightness = 15
            options.gpio_slowdown = 2
            options.drop_privileges = 0

        self.matrix = RGBMatrix(options = options)


    def run(self, message):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("Assets/tom-thumb.bdf")
        text_color = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        my_text = message
        counter = (len(my_text) * 4 + 65) * 3
        while counter >=0:
            offscreen_canvas.Clear()
            lens = graphics.DrawText(offscreen_canvas, font, pos, 31, text_color, my_text)
            pos -= 1
            if pos + lens < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            counter -= 1


    def scroll(self, matrix, font, color, message):
        pos = 65
        message_len = len(message) * 4 + pos
        for _ in message_len:
            graphics.DrawText(matrix, font, pos, 31, color, message)
            pos = pos - 1
            time.sleep(0.05)
