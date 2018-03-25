from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from multiprocessing import Value, Process, Queue, Array
import time

def subproc(matrix):
    matrix.SetPixel(25, 2, 0, 255, 0)
    matrix.SetPixel(25, 3, 0, 255, 0)
    matrix.SetPixel(25, 4, 0, 255, 0)
    matrix.SetPixel(25, 5, 0, 255, 0)
    print('print subproc')

# RGBMatrix Options
options = RGBMatrixOptions()
options.rows = 32
options.chain_length = 2
options.brightness = 20
options.gpio_slowdown = 2
options.drop_privileges = 0

# Create matrix with optiosn
matrix = RGBMatrix(options=options)

matrix.SetPixel(23, 2, 0, 0, 255)
matrix.SetPixel(23, 3, 0, 0, 255)
matrix.SetPixel(23, 4, 0, 0, 255)
matrix.SetPixel(23, 5, 0, 0, 255)
print('print main')

scroll_process = Process(target=subproc, args=(matrix,))
scroll_process.start()

time.sleep(999)
