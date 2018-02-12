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

        self.matrix = RGBMatrix(options=options)

    def run(self, message):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("Assets/tom-thumb.bdf")
        text_color = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        my_text = message
        counter = (len(my_text) * 4 + 65) * 3
        while counter >= 0:
            offscreen_canvas.Clear()
            lens = graphics.DrawText(
                offscreen_canvas, font, pos, 31, text_color, my_text)
            pos -= 1
            if pos + lens < 0:
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)
            counter -= 1

    def scroll(self, matrix, font, y, color, message, border_pixels=None):
        if not border_pixels:
            border_pixels = []
        pos = 65
        char_height = 5
        message_len = list(range(len(message) * 4 + pos))
        for _ in message_len:
            for x_idx, _ in enumerate(list(range(64))):
                for y_idx, _ in enumerate(list(range(char_height))):
                    y_pixel = y - 1 - y_idx
                    #print([x_idx, y_idx])
                    if [x_idx, y_pixel] not in border_pixels:
                        #print([x_idx, y_pixel])
                        matrix.SetPixel(x_idx, y_pixel, 0, 0, 0)
            graphics.DrawText(matrix, font, pos, y, color, message)
            pos = pos - 1
            time.sleep(0.05)
