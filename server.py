import socket
from threading import Thread

TCP_IP = 'localhost'
TCP_PORT = 1234
BUFFER_SIZE = 1024

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print (" New thread started for "+ip+":"+str(port))

    def run(self):
        def checkEntryValidity(msg):

            if len(msg.split(" ")) != 2 and msg != "best-time":
                print("invalid message format")
                return False;
            if msg != "best-time":
                _nomFichierCoureur = recvMsg.split(" ")[0]
                _tempCoureur = recvMsg.split(" ")[1]
                n1 = "alitta-caouette"
                n2 = "anne-leon"
                n3 = "alfred-blanken" 
                expr = (_nomFichierCoureur != n1 and
                       _nomFichierCoureur != n2 and
                       _nomFichierCoureur != n3 )
                
                if expr:
                    print("invalid file name")
                    return False;
            
                
    
        while True:
            recvMsg = self.sock.recv(1024).decode()
            print(recvMsg)
            if recvMsg == "best-time":
                with open("best-time.txt", 'r') as f:
                    resp = f.read()
                    self.sock.send(resp.encode())
                continue
            
            if checkEntryValidity(recvMsg)==False:
                continue
            nomFichierCoureur = recvMsg.split(" ")[0]
            tempCoureur = recvMsg.split(" ")[1] +  "\n"
            with open(nomFichierCoureur+".txt", 'a') as f:
                f.write(tempCoureur)
            with open(nomFichierCoureur+".txt", 'r') as f:
                content = f.readlines()
                content.sort()
                print(content)
                with open("best-time.txt", 'r') as f:
                    content2 = f.readlines()
                    for idx, line in enumerate(content2):
                        if line.split(" ")[0] == nomFichierCoureur:
                            content2[idx] = nomFichierCoureur+" "+content[0]
                            with open("best-time.txt", 'w') as f:
                                f.writelines(content2)
                


tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(5)
    print ("Waiting for incoming connections...")
    (conn, (ip,port)) = tcpsock.accept()
    print ('Got connection from '), (ip,port)
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()
