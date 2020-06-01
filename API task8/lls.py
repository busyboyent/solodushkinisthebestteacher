#!/usr/bin/env python
# coding: utf-8
import os


class LocalLS:
    def files(self, path="."):
        for file in os.listdir(path):
            if os.path.isfile(os.path.join(path, file)):
                yield file

    def output(self, path="."):

        for file in self.files(path):
            print(file)
