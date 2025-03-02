import socket
import os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
h="192.168.1.5"
p=4444
e="utf-8"
s.connect((h,p))
print("Client connecté")
while True:
    com=s.recv(1024).decode(e).strip()
    if com == "down":
        name = s.recv(1024).decode(e).strip()
        size= os.path.getsize(name)
        
        with open(name,"rb") as file:
            c=0
            s.sendall(str(size).encode(e))
            while c < size:
                data=file.read()
                s.sendall(data)
                c+=len(data)
    if com == "upl":
        size = int(s.recv(1024).decode(e).strip())
        reg=s.recv(1024).decode(e).strip()
        
        with open(reg,"wb") as file:
            c=0
            while c < size:
                data = s.recv(1024)
                file.write(data)
                c+=len(data)
s.close()