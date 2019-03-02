from cryptography.fernet import Fernet
import socket

def decypher(key, cipher_key):
    private_key = ""
    length = len(key)
    i=0
    while(i<length):
        private_key += chr((ord(cipher_key[i])-ord(key[i]))%127)
        i += 1

    return private_key

s = socket.socket();
s.bind(('', 9500))
s.listen(1)

c, addr = s.accept()
print('Got connection from', addr)

msg = "I am a military inteligent, you can trust me.";
key = Fernet.generate_key().decode()
cert = msg + key

c.send(cert.encode())

response = c.recv(1024).decode()
if response == "goodbye":
    print("shutting down")
    c.close()
else:
    cipher_key = response
    private_key = decypher(key, cipher_key)

    f = Fernet(private_key)
    encrypted = c.recv(1024)
    secret = f.decrypt(encrypted).decode()
    print("confirmed: " + secret)
    
    c.close()
