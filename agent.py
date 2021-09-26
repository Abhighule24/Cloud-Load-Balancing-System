# Link
# http://localhost:8080/?func=ping&params={"values":["ping","SD","CF"]}

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import json
import time
import threading
import local_agent
import socket

serverPort = 8080
host_get = socket.gethostname()
hostname = socket.gethostbyname(host_get)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    pass

class MyServer(BaseHTTPRequestHandler):
    def Stop_Serv():
        local_agent.running = False
        return("Server Stopped")
        
    def get_card(self,abc):
        xyz = json.loads(abc).get("values")
        card_report = {}
        for (i, j) in local_agent.report_card.items():
            #print(i)
            try:
                if len([x for x in xyz if x in j["Functions"]])>1:
                    card_report[i] = j
            except KeyError:
                pass
        return card_report

    agnt_func = {"Card": get_card, "Stop": Stop_Serv}

    def do_GET(self):
        print('Got a Request')
        self.send_response(200)
        self.send_header("Content-type", "text/JSON")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        try:
            otpt = self.wordLyz(self.path)
            if otpt.get("func") == "Card":  
                print(otpt.get('params'))
                #self.wfile.write(bytes("{ Report_card :"+str()+"\"}","utf-8"))
                self.wfile.write(bytes("{ \"Report_card\" :"+str(self.get_card(otpt.get('params')))+"}","utf-8"))
            elif otpt.get("func") == "Stop":
                self.wfile.write(bytes(str(self.agnt_func['Stop']()),"utf-8"))
        except IndexError:
            print('')
    


    def wordLyz(self,bulk):
        bulk = bulk.replace("%20"," ")
        bulk = bulk.replace("%22","\"")
        bulk = bulk.replace("%27","\'")
        bulk = bulk.replace("%5D","]")
        bulk = bulk.replace("%5B","[")
        bulk = bulk.replace("%7D","}")
        bulk = bulk.replace("%2C",",")
        bulk = bulk.replace("%7B","{")
        bulk = bulk.replace("%3A",":")
        wordz = bulk.split("/?")[1].split("&")
        print("full query: "+str(wordz))
        paramz = ["status","ok"]
        for paramx in wordz:
            for paramy in paramx.split("="):
                paramz.append(paramy)
        #paramz = wordz[1].split("=")
        print("param list: "+str(paramz))
        return self.dictConvert(paramz)
    
    def dictConvert(self,lst):
        res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
        return res_dct

if __name__ == "__main__":  
    webServer = ThreadedHTTPServer((hostname, serverPort),MyServer)
    print("Cloud local_agent started on http://%s:%s" % (hostname, serverPort))
    try:
        local_agent.py_agt().start()
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    webServer.server_close()
    print("Server stopped.")