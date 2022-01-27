import sys
from socket import *

if len(sys.argv) <= 1:
    print(
        "Usage: 'python proxyServer.py server_ip'\n[server_ip]: It is the IP address of proxy server"
    )
    sys.exit(2)

port = 8888
tcpSerSock = socket(AF_INET, SOCK_STREAM)
tcpSerSock.bind(("", port))
tcpSerSock.listen(1)

while 1:
    print("Ready to serve...")
    tcpCliSock, addr = tcpSerSock.accept()
    print("Recieved a connection from: ", addr)
    message = tcpCliSock.recv(1024).decode()
    filename = message.split()[1].partition("/")[2]
    print(filename)
    fileExist = False
    fileToUse = "/" + filename
    try:
        f = open(fileToUse[1:], "r")
        outputData = f.readlines()
        fileExist = True
        tcpCliSock.send("HTTP/1.0 200 OK\r\n".encode())
        tcpCliSock.send("Content-Type:text/html\r\n".encode())
        for line in outputData:
            tcpCliSock.send((line + "\r\n").encode())
        print("Read from cache")
    except IOError:
        if not fileExist:
            c = socket(AF_INET, SOCK_STREAM)
            hostn = filename.replace("www.", "", 1)
            try:
                c.connect((hostn, 80))
                fileObj = c.makefile("rw", None)
                fileObj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")
                fileObj.flush()
                buff = fileObj.readlines()
                print("done buff", buff)
                tmpFile = open("./" + filename, "wb")
                print("done tmpFile")
                for line in buff:
                    tmpFile.write(line.encode())
                print("done tmpFile.write")
                tcpCliSock.send("".join(buff).encode())
            except Exception as e:
                print(e)
                print("Illegal request")
        else:
            tcpCliSock.send("HTTP/1.0 404 NOT FOUND\r\n")
    tcpCliSock.close()
