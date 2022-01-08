import sys
import time
from socket import *

serverSocket = socket(AF_INET, SOCK_STREAM)
serverPort = int(sys.argv[1])
serverSocket.bind(("", serverPort))
serverSocket.listen(1)


def buildResponse(responseCode):
    if responseCode == 200:
        response = "HTTP/1.1 200 OK\n"
    elif responseCode == 404:
        response = "HTTP/1.1 404 Not Found\n"
    response += "Connection: close\n"
    time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    response += "Date: {now}\n".format(now=time_now)
    response += "Server: Simple-Python-Server\n"
    response += "Content-Type: text/html\n"
    response += "\r\n"
    return response


while True:
    print("Ready to serve...")
    connectionSocket, addr = serverSocket.accept()
    try:
        message = connectionSocket.recv(1024).decode()
        filename = message.split()[1][1:]
        f = open(filename)
        outputdata = f.read()
        response = buildResponse(200)
        response += outputdata
        connectionSocket.send(response.encode())
        connectionSocket.close()
    except IOError:
        response = buildResponse(404)
        connectionSocket.send(response.encode())
        connectionSocket.close()
