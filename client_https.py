import socket, ssl, pprint


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


# Require a certificate from the server. We used a self-signed certificate
# so here ca_certs must be the server certificate itself.
ssl_sock = ssl.wrap_socket(s,
                           ca_certs="server.crt",
                           cert_reqs=ssl.CERT_REQUIRED)

ssl_sock.connect(('localhost', 20000))

print repr(ssl_sock.getpeername())
print ssl_sock.cipher()
print pprint.pformat(ssl_sock.getpeercert())


if True: # from the Python 2.7.3 docs
    # Set a simple HTTP request -- use httplib in actual code.



    #          ssl_sock.write("""CONNECT HTTP/1.0\r\n
    # Host: login.iiit.ac.in\r\n\r\n""")


    
    ssl_sock.write("""GET / HTTP/1.0\r\n
    Host: login.iiit.ac.in\r\n\r\n""")
    while True:

        data = ssl_sock.read()
        if data:
            print data
        else:
            break


    
    

    # Read a chunk of data.  Will not necessarily
    # read all the data returned by the server.

    # note that closing the SSLSocket will also close the underlying socket
    ssl_sock.close()