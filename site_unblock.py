from SocketServer import BaseRequestHandler, ThreadingTCPServer
from socket import *
import time
import string

def methodCheck(data):
    method = ['GET', 'POST', 'HEAD', 'PUT', 'DELETE', 'OPTIONS']
    for name in method:
        if(data[0:len(name)] == name):
            return 1
    return 0

def getHTTPHostName(data): # Get Host Name From HTTP REQUEST Packet
    tmp = data.split(' ')
    return tmp[1][7:-1]

class SockHandler(BaseRequestHandler):
    def handle(self):
        self.data = self.request.recv(1024)
        print '[+]Received Data From Client...\n\n'
        f = methodCheck(self.data)
     
        if(f):
            hostName = getHTTPHostName(self.data)
			#print self.data
            dummyRequest = 'GET / HTTP/1.1\r\nHost: test.gilgil.net\r\n\r\n'
            self.data = dummyRequest + self.data
			#print self.data
            
            try:
                sock = socket(AF_INET, SOCK_STREAM)
                sock.connect((hostName, 80))
                sock.sendall(self.data)
                print '[+]Send Request to Server...\n\n'

                while(True):
                    received = sock.recv(4096)
                    if received.count('HTTP/1.1') > 1:
                        received = received[1:]
                        idx = received.find('HTTP/1.1')
                        received = received[idx:]
                    print '[+]Receiving Data From Server...\n\n'
                       
                    if not received:break
                    self.request.sendall(received)
            except:
                print "[+]Trying Connection...\n\n"
            finally:
                sock.close()


if __name__ == '__main__':
    proxy = ThreadingTCPServer(('127.0.0.1', 8081), SockHandler)
    proxy.stop_looping = False
    try: proxy.serve_forever()
    except KeyboardInterrupt: print 'ctrl+c'
    proxy.stop_looping = True
