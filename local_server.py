import socket
import threading
import time
import servfunc

def run_server(report_card, serv_name):
    class Server(threading.Thread):
        def __init__(self, obj, host, port):
            threading.Thread.__init__(self)
            self.obj = obj
            self.host = host
            self.port = port

        def run(self):
            self.obj.connect((self.host, self.port))
            print(self.obj.recv(1024).decode())
            self.obj.send(serv_name.encode())

            while True:
                serv_x = threading.Thread(servfunc.AgentWork(self.obj, self.port, report_card)) #, 0))
                serv_x.start()

    s = socket.socket()
    host = '154.61.75.17'
    port = 12345
    Server(s, host, port).start()
if __name__ == "__main__":
    print("This code doesn't run individually")
    #serv_A({'Allocation': 10, 'Functions': ['ping','dataset','SD','ED','CF' ,'anova']})