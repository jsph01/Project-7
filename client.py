from cryptography.fernet import Fernet
import socket

def cipher(key1, key2):
    cipher_key = ""

    length = len(key1)
    i = 0
    while(i < length):
        cipher_key += chr((ord(key1[i])+ord(key2[i]))%127)
        i += 1

    return cipher_key
    

s = socket.socket()
s.connect (('127.0.0.1', 9500))

s2 = socket.socket()
s2.connect (('127.0.0.1', 9501))
cert = s.recv(1024)

s2.send(cert)
validation = s2.recv(1024).decode()
s2.close()

if validation == "invalid":
    s.send("goodbye".encode())
    s.close()
else:
    cert = cert.decode()
    ind = cert.find('.')
    
    public_key = cert[ind+1:]
    private_key = Fernet.generate_key().decode()
    cipher_key = cipher(public_key, private_key)
    
    s.send(cipher_key.encode())

    f = Fernet(private_key)
    secret = "London bridge is down".encode()
    encrypted = f.encrypt(secret)
    print(f.decrypt(encrypted).decode())
    s.send(encrypted)

    

    

s.close()
