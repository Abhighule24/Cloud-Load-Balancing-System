# Link
# http://20.185.36.169:10101/?func=SD&params={"values":[1,2,3]}

from http.server import BaseHTTPRequestHandler, HTTPServer
from socketserver import ThreadingMixIn
import time
import threading
import json
import socket
import servfunc
import local_server

def run_server(serv_name, port, allocation, functions):
    
    func_name = ['dataset','SD','ED','CF' ,'anova']
    func_call = [servfunc.dataset, servfunc.standard_deviation, servfunc.Euclidean_distance, servfunc.cumulative_freq, servfunc.anova]
    global func_dict
    func_dict = {'ping': servfunc.sping}
    func_list = ['ping']
    for n in functions:
        func_dict[func_name[int(n)-1]] = func_call[int(n)-1]
        func_list.append(func_name[int(n)-1])

    host_get = socket.gethostname()
    hostname = socket.gethostbyname(host_get)
    port, allocation = int(port), int(allocation)
    
    report_card = {'ip': hostname, 'port': port,'Allocation': allocation, 'Functions': func_list}
    
    print(serv_name,"\nDemo Link")
    print('http://'+hostname+':'+str(port)+'/?func=SD&params={"values":[1,2,3]}')
    
    class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
        pass

    class MyServer(BaseHTTPRequestHandler):
        def do_GET(self):
            if report_card['Allocation'] > 0:
                report_card['Allocation'] = report_card['Allocation']-1
                print(report_card['Allocation'])
                self.send_response(200)
                self.send_header("Content-type", "text/JSON")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                print("Sleeping Now")
                time.sleep(0.08)
                print("Awake")
                try:
                    otpt = self.wordLyz(self.path)
                    self.wfile.write(bytes("{ \"status\": \"success\",\"output\": \""+func_dict[otpt.get("func")](otpt.get('params'))+"\"}","utf-8"))
                
                except IndexError:
                    self.wfile.write(bytes("{status: \"fail\",details: \"params not found\"}", "utf-8"))
                print("sent reply for: ")
                try:
                    print(self.wordLyz(self.path))
                except TypeError:
                    print("Error Occured.")
                except IndexError:
                    print("unwanted error ignored")
                print("==================")
                
                report_card['Allocation'] = report_card['Allocation'] + 1
                print(report_card['Allocation'])

        def wordLyz(self,bulk):
            bulk = bulk.replace("%20"," ")
            bulk = bulk.replace("%22","\"")
            bulk = bulk.replace("%27","\'")
            wordz = bulk.split("/?")[1].split("&")
            print("full query: "+str(wordz))
            paramz = ["status","ok"]
            for paramx in wordz:
                for paramy in paramx.split("="):
                    paramz.append(paramy)
            print("param list: "+str(paramz))
            return self.dictConvert(paramz)

        def dictConvert(self,lst):
            res_dct = {lst[i]: lst[i + 1] for i in range(0, len(lst), 2)}
            return res_dct



        
    webServer = ThreadedHTTPServer((hostname, port),MyServer)
    print("Server started http://%s:%s" % (hostname, port))
    try:
        threading.Thread(local_server.run_server(report_card, serv_name)).start()
        webServer.serve_forever()
    except KeyboardInterrupt:
        pass
    
    webServer.server_close()
    print("Server stopped.")

if __name__ == "__main__":
    print("Enter parameters with space:")
    usr_ip = input()
    serv_name, port, allocation, functions = tuple(usr_ip.split(" "))
    print(serv_name)
    functions = functions.split(",")
    run_server(str(serv_name), port, allocation, functions)