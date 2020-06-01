#!/usr/bin/env python
# coding: utf-8
import urllib.parse
from main import *
from lls import *
from catalog import *
from archive import *


class ProgramBody:
    def __init__(self, method, comand_list):
        self.method = method
        self.list = comand_list

    def help_info(self):
        return (
            "пожалуйста выберите команду из списка:\n" +
            "mkdir создать директорию Пример: mkdir; fold\n" +
            "remove удалить файл/директорию" +
            " Пример: remove; fold\n" +
            "ls\n" +
            "download скачать файл" +
            " Пример: download; /path; filename\n" +
            "upload загрузить файл " +
            "Пример: upload; file; /path/filename\n" +
            "lls\n" +
            "catalog загрузить каталог" +
            "Пример: catalog; folder\n" +
            "exit Введите exit для выхода" +
            "archive архивирует файл и заливает его на диск " +
            "Пример: archive; file; /path/filename\n" +
            "unpack разпаковывает архив\n" +
            "\nSPECIAL FOR MAKS: archive; sky.py; /sky.zip\n" +
            "upload; sky.py; /sky.py\n" +
            "после этих команд можно проверить download\n" +
            "download; /sky.py; sky1.py"
        )

    def switch_case(self, case):
        self.help = self.help_info()
        self.lls = LocalLS()
        error_text = "недостаточно аргументов в команде, обратитесь к help"
        if case == "mkdir":
            if len(self.list) == 2:
                self.method.mkdir(self.list[1])
                return("mkdir")
            else:
                print(error_text)
        elif case == "remove":
            if len(self.list) == 2:
                self.method.remove(self.list[1])
                return("remove")
            else:
                print(error_text)
        elif case == "upload":
            if len(self.list) == 3:
                self.method.upload(self.list[1], self.list[2])
                return("upload")
            else:
                print(error_text)
        elif case == "download":
            if len(self.list) == 3:
                path = urllib.parse.quote(self.list[1])
                self.method.download(path, self.list[2])
                return("download")
            else:
                print(error_text)
        elif case == "ls":
            if len(self.list) == 1:
                self.method.ls()
                return("ls")
            elif len(self.list) == 2:
                self.method.ls(self.list[1])
                return("ls")
            else:
                print(error_text)
        elif case == "catalog":
            if len(self.list) == 2:
                self.catalog = UploadCatalog(self.list[1], self.method)
                self.catalog.upload_catalog()
                return("catalog")
            else:
                print(error_text)
        elif case == "archive":
            if len(self.list) == 3:
                archive = Archive(self.list[1])
                file = archive.get_archive()
                self.method.upload(file, self.list[2])
                return("archive")
            else:
                print(error_text)
        elif case == "unpack":
            if len(self.list) == 2:
                archive = Archive(self.list[1])
                archive.get_file()
                return("unpack")
            else:
                print(error_text)
        elif case == "lls":
            if len(self.list) == 1:
                self.lls.output()
                return("lls")
            else:
                self.lls.output(self.list[1])
                return("lls")
        elif case != "exit":
            print(self.help)
            return ("help")
