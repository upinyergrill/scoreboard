from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
from threading import Thread
import time

def subproc(matrix):
    for i in range(1,10):
        matrix.SetPixel(25, i, 0, 255, 0)
        time.sleep(1)
    print('print subproc')

class myThread (Thread):
    def __init__(self, matrix):
        Thread.__init__(self)
        self.matrix = matrix

    def run(self):
        print("Starting " + self.name)
        subproc(self.matrix)
        print("Exiting " + self.name)

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

# Create new threads
thread1 = myThread(matrix)

# Start new Threads
thread1.start()

print("Exiting Main Thread")


#scroll_process = Process(target=subproc, args=(matrix,))
#scroll_process.start()

time.sleep(1)
print('after sleep')
