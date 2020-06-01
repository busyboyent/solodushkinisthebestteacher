#!/usr/bin/env python
# coding: utf-8
import time
import urllib
import sys
from sys import stdin, exit as sys_exit
from sky import *
from dropbox import *
from text import *
from programBody import *
from getToken import *
from threading import Thread


class Main(object):

    mod = None
    start_time = 0
    def __init__(self):

        self.authorization()

    def get_mod(self):

        messege = (
            "для использования yandex disk введите y," +
            " для использования dropbox введите d [y/d]"
        )
        print(messege)

        self.mod = input()
        return "gj"

    def authorization(self):

        if len(sys.argv) == 2:
            if sys.argv[1] == "--help":
                txt = Text()
                print(txt.help_start)
                sys_exit()
            if sys.argv[1] == "reset":
                with open("Token.txt", "w") as f:
                    f.write("None")
                with open("TokenDrop.txt", "w") as f:
                    f.write("None")
            if sys.argv[1] == "yandex":
                self.mod = "y"
            if sys.argv[1] == "dropbox":
                self.mod = "d"

        while True:
            if self.mod == "y" or self.mod == "d":
                break
            self.get_mod()

        if self.mod == "y":

            with open("Token.txt", "r+") as f:

                self.get_token = f.read()

                if self.get_token == "None":
                    f.seek(0)
                    self.token = GetToken()

                    print("пожалуйста перейдите по ссылке для авторизации:")
                    print(self.token.get_url_authorize())

                    self.get_token = self.token.get_token()

                    f.write(self.get_token)

            self.token = YaDisk(self.get_token)

            self.program_cycle(self.token)

        elif self.mod == "d":

            with open("TokenDrop.txt", "r+") as f:

                self.get_token = f.read()

                if self.get_token == "None":
                    f.seek(0)
                    self.token = GetToken()

                    print("пожалуйста перейдите по ссылке для авторизации:")
                    print(self.token.get_url_dropbox())

                    self.get_token = self.token.get_token()

                    f.write(self.get_token)

            self.token = Dropbox(self.get_token)

            self.program_cycle(self.token)
        return "gj"

    def program_cycle(self, method):

        self.flag = True

        while self.flag:

            self.start_time = time.time()
            print("\n")
            print("Введите команду для выполнения:")

            self.command_list = input().split("; ")
            print("\n")

            if self.command_list[0] == "exit":
                self.flag = False

            self.circle_body = ProgramBody(method, self.command_list)

            self.circle_body.switch_case(self.command_list[0])

            try:
                urllib.request.urlopen("http://google.com")
            except IOError:
                "Google is not available! Internet is broken!"
        return "gj"


if __name__ == "__main__":

    ex = Main()
