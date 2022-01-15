import base64
import ssl
import sys
from socket import *

msg = "\r\n I love computer networks!"
endmsg = "\r\n.\r\n"

mailserver = ("smtp.gmail.com", 465)

clientSocket = ssl.wrap_socket(socket(AF_INET, SOCK_STREAM))
clientSocket.connect(mailserver)

recv = clientSocket.recv(1024).decode()
print(recv)
if recv[:3] != "220":
    print("220 reply not received from server.")

heloCommand = "HELO Alice\r\n"
clientSocket.send(heloCommand.encode())
recv1 = clientSocket.recv(1024).decode()
print(recv1)
if recv1[:3] != "250":
    print("250 reply not received from server.")

# Authenticate.
username = sys.argv[1]
password = sys.argv[2]
recipient = sys.argv[3]
clientSocket.send("AUTH LOGIN\r\n".encode())
print(clientSocket.recv(1024))
clientSocket.send(base64.b64encode(username.encode()) + "\r\n".encode())
print(clientSocket.recv(1024))
clientSocket.send(base64.b64encode(password.encode()) + "\r\n".encode())
print(clientSocket.recv(1024))

clientSocket.send(("MAIL FROM: <" + username + ">\r\n").encode())
print(clientSocket.recv(1024))

clientSocket.send(("RCPT TO: <" + recipient + ">\r\n").encode())
print(clientSocket.recv(1024))

clientSocket.send("DATA\r\n".encode())
print(clientSocket.recv(1024))

clientSocket.send((msg + endmsg).encode())
print(clientSocket.recv(1024))

clientSocket.send("QUIT\r\n".encode())
print(clientSocket.recv(1024))
