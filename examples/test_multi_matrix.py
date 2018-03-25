from rgbmatrix import RGBMatrix, graphics, RGBMatrixOptions
import threading
import time


def subproc(matrix):
    matrix.SetPixel(25, 2, 0, 255, 0)
    matrix.SetPixel(25, 3, 0, 255, 0)
    matrix.SetPixel(25, 4, 0, 255, 0)
    matrix.SetPixel(25, 5, 0, 255, 0)
    print('print subproc')

exitFlag = 0


class myThread (threading.Thread):
    def __init__(self, threadID, name, counter):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter

    def run(self):
        print("Starting " + self.name)
        print_time(self.name, self.counter, 5)
        print("Exiting " + self.name)


def print_time(threadName, delay, counter):
    while counter:
        if exitFlag:
            threadName.exit()
        time.sleep(delay)
        print("%s: %s" % (threadName, time.ctime(time.time())))
        counter -= 1


# Create new threads
thread1 = myThread(1, "Thread-1", 1)
thread2 = myThread(2, "Thread-2", 2)

# Start new Threads
thread1.start()
thread2.start()
thread1.join()
thread2.join()
print("Exiting Main Thread")

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

#scroll_process = Process(target=subproc, args=(matrix,))
#scroll_process.start()

#time.sleep(999)
