import time
from socket import *

serverName = "localhost"
serverPort = 12000
clientSocket = socket(AF_INET, SOCK_DGRAM)
clientSocket.settimeout(1)
for i in range(1, 11):
    time_now = time.strftime("%a, %d %b %Y %H:%M:%S", time.localtime())
    message = "Ping {i} {now}".format(i=i, now=time_now)
    try:
        start = time.time()
        clientSocket.sendto(message.encode(), (serverName, serverPort))
        modifiedMessage, serverAddress = clientSocket.recvfrom(2048)
        end = time.time()
        print(
            "From Server: {message}. RTT: {rtt} seconds".format(
                message=modifiedMessage.decode(), rtt=end - start
            )
        )
    except timeout:
        print("Request {i} timeout".format(i=i))
        continue
clientSocket.close()
