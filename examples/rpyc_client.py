import time
import rpyc

# rpyc client
conn = rpyc.connect("localhost", 12345)
c = conn.root

# do stuff over rpyc
print('update =', c.get_main_update())
# calling a method of the remote service
print('testing returned:', c.testthings(66))  
