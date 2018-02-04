import os
import sys
import random
import time
import base64

if len(sys.argv) < 4:
    print "Usage: python client.py <CLIENT_PORTS_RANGE> <PROXY_PORT> <END_SERVER_PORT>"
    print "Example: python client.py 20010 20000 19990-19999"
    raise SystemExit

CLIENT_PORT = sys.argv[1]
PROXY_PORT = sys.argv[2]
SERVER_PORT = sys.argv[3]

D = {0: "GET", 1:"POST"}

while True:
    filename = "%d.data" % (int(random.random()*9)+1)
    METHOD = D[int(random.random()*len(D))]
    USERNAME = "admin"
    PASSWORD = "admin"
    PASS = base64.b64encode(USERNAME+':'+PASSWORD)
    AUTH =  '"Authentication: Basic '+PASS+'"' 
    print AUTH
    os.system("curl --request %s -H %s --proxy 127.0.0.1:%s --local-port %s 127.0.0.1:%s/%s" % (METHOD, AUTH, PROXY_PORT, CLIENT_PORT, SERVER_PORT, filename))
    time.sleep(10)

