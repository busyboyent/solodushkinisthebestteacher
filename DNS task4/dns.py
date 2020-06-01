import time
import sys
import socket
import requests
import dnslib
import os
import pickle


class Main:

    def __init__(self):

        self.start()
    
    def start(self):
        server = Server()

        print("server has started working")
        server.upload_cash()
        try:
            while True:
                server.make_request()
                server.take_receive()
                time.sleep(0.2)
                server.check_TTL()
        except KeyboardInterrupt:
            print("server successfully finished working")
        except Exception as e:
            print("server is shut down due to an error")
            print(e)
        finally:
            server.request_socket.close()
            server.receive_socket.close()
            with open('cache.txt', 'wb') as f:
                pickle.dump(server.cache, f)
            time.sleep(1)
            sys.exit(0)


class Server():

    def __init__(self):

        self.cache = {}
        self.request_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.request_socket.bind(('localhost', 53))
        self.request_socket.settimeout(0)
        self.receive_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.receive_socket.settimeout(0)

    def upload_cash(self):
        with open('cache.txt', 'rb') as f:
            try:
                self.cache = pickle.load(f)
                self.check_TTL()
            except Exception:
                print('not found cache file')

    def make_request(self):
        try:
            data, address = self.request_socket.recvfrom(1024)
        except OSError:
            data = None
        if data:
            answer = dnslib.DNSRecord.parse(data)
            question = answer.questions[0]
            if question.qname in self.cache:
                cache, ttl = self.cache[question.qname]
                print('cache ' + str(question.qname) + ' ttl ' + str(time.ctime(ttl)))
                print(cache)
                answer.questions.remove(question)
            else:
                print('record ' + str(question.qname))
            if answer.question:
                server = ("8.8.8.8", 53)
                self.receive_socket.sendto(answer.pack(), server)

    def take_receive(self):
        try:
            data, address = self.receive_socket.recvfrom(1024)
        except OSError:
            data = None
        if(data):
            answer = dnslib.DNSRecord.parse(data)
            print(answer)
            for question in answer.rr:
                self.cache[question.rname]= (answer, int(time.time()) + question.ttl)

    def check_TTL(self):
        for i in self.cache:
            cache, ttl = self.cache[i]
            if ttl < int(time.time()):
                del self.cache[i]


if __name__ == "__main__":

    ex = Main()