import time
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions


class ScrollableText(object):
    def scroll(self, matrix, font, y, color, message, border_pixels=None, border_color=None, break_loop=None):
        if not border_pixels:
            border_pixels = []
        pos = 65
        char_height = 5
        message_len = list(range(len(message) * 4 + 65))
        for _ in message_len:
            # using shared memory value
            if break_loop:
                if bool(break_loop.value) is True:
                    break
            for x_idx, _ in enumerate(list(range(64))):
                for y_idx, _ in enumerate(list(range(char_height))):
                    y_pixel = y - 1 - y_idx
                    if [x_idx, y_pixel] not in border_pixels:
                        matrix.SetPixel(x_idx, y_pixel, 0, 0, 0)
            graphics.DrawText(matrix, font, pos, y, color, message)
            if border_pixels and border_color:
                for pixel in border_pixels:
                    matrix.SetPixel(pixel[0], pixel[1], border_color['r'], border_color['g'], border_color['b'])
            pos = pos - 1
            time.sleep(0.05)
