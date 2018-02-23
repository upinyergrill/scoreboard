from multiprocessing import Process, Value, Array
import time
import os

def colors(r, g, b):
    while True:
        with r.get_lock():
            r.value += 1
        with g.get_lock():
            g.value += 1
        with b.get_lock():
            b.value += 1
        ''' r.value = r.value + 1
        g.value = g.value + 1
        b.value = b.value + 1 '''
        time.sleep(1)

def proc(r, g, b):
    while True:
        ''' with r.get_lock():
            r.value += 1
        with g.get_lock():
            g.value += 1
        with b.get_lock():
            b.value += 1 '''
        print('pid', os.getpid(), 'r:', r.value, 'g:', g.value, 'b:', b.value)
        time.sleep(1)

if __name__ == '__main__':
    r = Value('i', 253)
    g = Value('i', 184)
    b = Value('i', 39)
    c = Process(target=colors, args=(r,g,b,))
    c.start()

    procs = []
    for _ in [0,0,0]:
        p = Process(target=proc, args=(r,g,b,))
        p.start()
        procs.append(p)
        #print('end of loop')
    
    #for p in procs:
        #p.join()

    c.join()

    #print('r:', r.value, 'g:', g.value, 'b:', b.value)
