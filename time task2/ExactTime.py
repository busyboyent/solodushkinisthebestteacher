import requests
import time
import re
import socket
import sys


class Server:

    def __init__(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.test_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.server.bind(('localhost', 53))
        self.server.settimeout(0)
        self.test_socket.settimeout(0)

    def get_time(self):
        url = "https://www.timeserver.ru/"
        time_url = requests.get(url)
        rep = int(re.search(r'utcTime: ?([^,>]+)', time_url.content.decode('utf-8')).group(1)[:-3])

        with open('sabotage.txt', "r") as f:
            plus_time = int(f.read())

        result = time.gmtime(rep+plus_time)

        print('UTC time', result.tm_hour, result.tm_min, result.tm_sec, result, sep=':')
        return result

    def take_receive(self):
        data, addr = self.server.recvfrom(1024)
        exact_time = get_time()
        if data:
            self.server.sendto(bytes(exact_time, encoding = "utf-8"), addr)


server = Server()
try:
    while True:
        server.take_receive()
except KeyboardInterrupt:
    print("done")
except Exception:
    print("error")
finally:
    server.server.close()
    server.test_socket.close()
    time.sleep(1)
    sys.exit(0)
