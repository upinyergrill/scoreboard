#!/usr/bin/env python
# Display a runtext with double-buffering.
from samplebase import SampleBase
from rgbmatrix import graphics, RGBMatrix, RGBMatrixOptions
import time

# RGBMatrix Options
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.brightness = 15
options.gpio_slowdown = 2
options.drop_privileges = 0

matrix = RGBMatrix(options = options)

class RunText(SampleBase):
    def __init__(self, *args, **kwargs):
        super(RunText, self).__init__(*args, **kwargs)
        self.parser.add_argument("-t", "--text", help="The text to scroll on the RGB LED panel", default="Hello world!")

    def run(self):
        offscreen_canvas = matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont("Assets/tom-thumb.bdf")
        textColor = graphics.Color(255, 255, 255)
        pos = offscreen_canvas.width
        my_text = self.args.text
        counter = (len(my_text) * 4 + 65) * 3
        while counter >=0:
            offscreen_canvas.Clear()
            lens = graphics.DrawText(offscreen_canvas, font, pos, 31, textColor, my_text)
            pos -= 1
            if (pos + lens < 0):
                pos = offscreen_canvas.width

            time.sleep(0.05)
            offscreen_canvas = matrix.SwapOnVSync(offscreen_canvas)
            counter -= 1


# Main function
if __name__ == "__main__":
    run_text = RunText()
    if (not run_text.process()):
        run_text.print_help()
