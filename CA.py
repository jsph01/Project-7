import socket

# open port 9501 for communication
s = socket.socket();
s.bind(('', 9501))
s.listen(1)

# accept an incomming connection from the client
c, addr = s.accept()
print('Got connection from', addr)

# recieve a certificate from the client
msg = c.recv(1024).decode();

# if the CA finds "you can trust me" somewhere in the certificate,
# then it will determine that the source of the certificate is legitimate
if msg.find("you can trust me") >= 0:
    c.send("valid".encode())
else:
    c.send("invalid".encode())

# end connection with the client
c.close()
