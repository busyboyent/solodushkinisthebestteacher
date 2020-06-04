import socket
import threading
import psutil
from random import randint


def getfreeport():
    port = randint(49152,65535)
    portsinuse=[]
    while True:
        conns = psutil.net_connections()
        for conn in conns:
            portsinuse.append(conn.laddr[1])
        if port in portsinuse:
            port = randint(49152,65535)
        else:
            break
    return port

#def scan_port(ip, port):
#  sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
##  sock.settimeout(0.5)
##  try:
#    connect = sock.connect((ip,port))
#     print('Port :',port,' its open.')
#     connect.close()
#  except:
#     pass

def get_open_port():

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("",0))
    s.listen(1)
    port = s.getsockname()[1]
    s.close()
    return port

ip = 'введите ip'


answer = get_open_port()
print(answer)

print(getfreeport())