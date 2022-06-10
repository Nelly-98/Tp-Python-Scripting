import socket
import time
from threading import Thread

TCP_IP = 'localhost'
TCP_PORT = 1234
BUFFER_SIZE = 1024

global timeLimit
global startTime
global elapsedTime
global isInputLocked

timeLimit = 5
startTime = 0
elapsedTime = 0
isInputLocked = False
print("Mots-clés: fin, best-time")
print("Coureurs valide: alitta-caouette, anne-leon, alfred-blanken \n")

class ReceptionThread(Thread):
    
    def __init__(self, sock):
        Thread.__init__(self)
        self.sock = sock
        print ("Reception thread started")

    def run(self):
        global isInputLocked
        
        while True:
            try:
                recvMsg = self.sock.recv(1024).decode()
                isInputLocked = False
                print(recvMsg + "\n")
            except:
                print("Thread closed")
                break
            
                
class WritingThread(Thread):
    
    
    def __init__(self,sock):
        Thread.__init__(self)
        self.sock = sock
        print ("Writing thread started \n")

    def run(self):
        global startTime
        global elapsedTime
        global isInputLocked
        def checkEntryValidity(msg):

            if len(msg.split(" ")) != 2 and msg != "best-time":
                print("invalid message format")
                return False;
            if msg != "best-time":
                _nomFichierCoureur = msg.split(" ")[0]
                _tempCoureur = msg.split(" ")[1]
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
            if isInputLocked and elapsedTime < timeLimit:
                if startTime == 0:
                    startTime = time.time()
                elapsedTime = time.time() - startTime
                continue
            startTime = 0
            elapsedTime = 0
            isInputLocked = False
            
            msg = input("Entrez le nom du coureur suivi de son temp: ")
            
            
            if msg == "fin":
                self.sock.close()
                print ("Fin de la connexion")
                break
            if checkEntryValidity(msg)==False and msg != "best-time" :
                continue
            else:
                if msg == "best-time":
                    isInputLocked = True
                msg = msg.encode()
                self.sock.send(msg)

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((TCP_IP, TCP_PORT))
threads = []

Rthread = ReceptionThread(sock)
Rthread.start()
threads.append(Rthread)

Wthread = WritingThread(sock)
Wthread.start()
threads.append(Wthread)

for t in threads:
    t.join()



