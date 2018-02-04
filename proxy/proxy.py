import socket
import threading
import sys
import re
import os
import time
from netaddr import IPNetwork
import base64
import ssl
import time
from filelock import FileLock
import httplib

REQ_LIST=[]
CACHE=[]
def retrieve_from_cache(response):
    if "304" in response:
        return True
    else:
        return False


def put_cache(client, filename, response):
    print filename
    with FileLock("cache/"+filename):
        with open("cache/"+filename, 'wb') as f:
            f.write(response)
    response_no_cache(client ,response)

def cache_condition(client, filename, response):
    global REQ_LIST
    global CACHE

    if("no-cache" not in response):
        req={}
        req['name'] = filename
        req['time'] = time.time()
        REQ_LIST.append(req)
        print req['time']
        till = req['time'] - 5 * 60 * 1000
        count = 0 
        print till
        for i in xrange(len(REQ_LIST)-1, 0, -1):
            if(REQ_LIST[i]['time']< till):
                break

            if(REQ_LIST[i]['name'] == filename):
                count+=1

        if(count >= 3):
            # files = os.listdir("cache/"+filename)
            if(len(CACHE)>=3):
                os.remove("cache/"+REQ_LIST[0]['name'])
                del CACHE[0]
            CACHE.append(req)
            put_cache(client, filename, response)
        else:
            response_no_cache(client, response)

        print REQ_LIST
        print CACHE
    else:
        response_no_cache(client, response)

def check_if_present(filename, req):
    exist = os.path.isfile("cache/"+filename)
    if(exist):
        file_time = time.ctime(os.path.getmtime("cache/"+filename))
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
    f = open("cache/"+filename , 'rb')
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
            client.settimeout(2)
            threading.Thread(target = self.listenToClient,args = (client,address)).start()

    def listenToClient(self, client, address):

        log = open('MitM_http.txt', "a")
        size = 1024
        
        #RECEIVING REQUEST FROM CLIENT
        c_req = ""
        while True:
            try:
                data = client.recv(size)
                if not data:
                    break
                c_req = c_req + data
            except:
                break

        log.write(c_req)
        c_req_split = re.split("://|:|/| ",c_req)
        print c_req_split
        temp = c_req
        c_req = c_req[:temp.find("http")]+c_req[temp.find("1/")+1:]
        print c_req

        filename = c_req_split[4]
        
        c_req = check_if_present(filename, c_req)



        https = False
        fake = False
        if(c_req.find('CONNECT') != -1):
            https = True
        print https

        if(not https):
            blacklist = False
            auth = False #Change to false during production 



            #Check for blacklisted server
            USERNAME = "admin"
            PASSWORD = "admin"
            PASS = base64.b64encode(USERNAME+':'+PASSWORD)
            print PASS

            with open('blacklist.txt') as f:
                for line in f:
                    if blacklist == True:
                        break
                    for ip in IPNetwork(line):
                        if(str(c_req_split[2]) == str(ip)):
                            print "Blacklisted IP"
                            blacklist = True

            PASS_REQ = c_req[c_req.find("Basic ")+6:]
            PASS_REQ = PASS_REQ[:PASS_REQ.find("\r")]
            print "REQUEST PASS : " + PASS_REQ
            if(PASS_REQ == PASS):
                print "Authenticated"
                auth = True
            if(blacklist == True and auth == False):
                client.sendall('HTTP/1.1 404 Page not found\nContent-Type: text/html\n\nBlacklisted Content\n\n')
                client.close()
    

        if(https and not fake):
            try:
                # If successful, send 200 code response
                server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                server_sock.settimeout(6)   
                server_sock.connect(( c_req_split[1], int(c_req_split[2]) ))
                reply = "HTTP/1.0 200 Connection established\r\n"
                reply += "Proxy-agent: Pyx\r\n"
                reply += "\r\n"

                print reply.encode()
                client.sendall( reply.encode() )

            except socket.error as err:
                # If the connection could not be established, exit
                # Should properly handle the exit with http error code here
                print(err)
                
#
            request = ""
            while True:
                try:
                    request += client.recv(size)
                except:
                    break
            server_sock.sendall( request )

            print "REQUEST:"
            print request

            reply=""
            while True:
                try:

                    reply += server_sock.recv(size)
                   
                except:
                    break

            print "REPLY:"
            print reply
            client.sendall( reply )

            


#
#
            request = ""
            while True:
                try:
                    request += client.recv(size)
                except:
                    break
            server_sock.sendall( request )

            print "REQUEST:"
            print request

            reply=""
            while True:
                try:

                    reply += server_sock.recv(size)
                   
                except:
                    break

            print "REPLY:"
            print reply
            client.sendall( reply )

            


#
#
            request = ""
            while True:
                try:
                    request += client.recv(size)
                except:
                    break
            server_sock.sendall( request )

            print "REQUEST:"
            print request

            reply=""
            while True:
                try:

                    reply += server_sock.recv(size)
                   
                except:
                    break

            print "REPLY:"
            print reply
            client.sendall( reply )

            


#
#
            request = ""
            while True:
                try:
                    request += client.recv(size)
                except:
                    break
            server_sock.sendall( request )

            print "REQUEST:"
            print request

            reply=""
            while True:
                try:

                    reply += server_sock.recv(size)
                   
                except:
                    break

            print "REPLY:"
            print reply
            client.sendall( reply )

            


#



            
            client.close()
            server_sock.close()

        elif(https and fake):
            # SET VARIABLES
            packet, reply = "<packet>SOME_DATA</packet>", ""

            # WRAP SOCKET
            connstream = ssl.wrap_socket(client, server_side=True, certfile="server.crt", keyfile="server.key")
           

            data = connstream.read()
            
            print data

            # CLOSE SOCKET CONNECTION
            connstream.close()

        #RESPONSE FROM SERVER TO CLIENT
        else:
             #SENDING REQUEST TO SERVER
            server_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server_sock.connect((c_req_split[2], int(c_req_split[3])))
            server_sock.settimeout(3)   
            server_sock.sendall(c_req)
            print " SEND TO SERVER : "
            print c_req
            response = ""
            while True:
                try:
                    data = server_sock.recv(size)
                    response += data
                    if not data:
                        break
                    # client.sendall(data)
                except:
                    break
            print "RESPONSE:"
            print response
            if(retrieve_from_cache(response)):
                print "here"
                response_cache(client, filename)
            else:
                cache_condition(client , filename, response)

            log.write(response)


            server_sock.close()
            client.close()
        log.close()




if __name__ == "__main__":
    port_num = input("Port? ")
    ThreadedServer('',port_num).listen()
   

