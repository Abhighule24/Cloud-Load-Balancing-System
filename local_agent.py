import socket                
import pickle
import threading
import time

report_card = {}

running = True
#report_card = {'Server A':{'Allocation': 5, 'Functions': ['ping','dataset','SD','ED','CF' ,'anova']},'Server B':{'Allocation': 10, 'Functions': ['ping','dataset','ED','anova']},'Server C':{'Allocation': 10, 'Functions': ['ping','SD','CF' ,'anova']}}
class CardReport(threading.Thread):
    def __init__(self, c, addr, card_report):
        threading.Thread.__init__(self)
        self.c = c
        self.addr = addr
        self.card_report = card_report 
    def run(self):
        print("Got connection from : ", self.addr)        
        self.c.send("Thank you for connecting".encode())
        serv_name = str(self.c.recv(7).decode())

        while True:
            ReportObj= self.c.recv(1024)
            #x = self.c.recv(1024).decode()
            card= pickle.loads(ReportObj)
            self.card_report[serv_name] = card
            print('\n',serv_name," : ", card)
            print(self.card_report,'\n') 

class py_agt(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        print("Agent Running to accept Server Requests")
        s = socket.socket()          
        port = 12345                
        s.bind(('154.61.75.17', port)) 
        s.listen(5)      
        thread_name = []
        while running: 
            c, addr = s.accept()      
            thread_name.append(CardReport(c, addr, report_card))
            thread_name[len(thread_name)-1].start()
        print("Agent Stopped")
if __name__ == "__main__":
    py_agt().start()