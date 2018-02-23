import time
import rpyc
from rpyc.utils.server import ThreadedServer
from threading import Thread
from multiprocessing import Process, Value, Array

class MyService(rpyc.Service):
    def exposed_testthings(self, x):
        r.value = r.value + x
        return r.value
    def exposed_get_main_update(self):
        return 7

# start the rpyc server
r = Value('i', 0)
server = ThreadedServer(MyService, port = 12345)
''' t = Thread(target = server.start)
t.daemon = False
t.start()
t.join() '''

c = Process(target=server.start)
c.start()
c.join()