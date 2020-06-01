import os
import re
from archive import *


class UploadCatalog:
    def __init__(self, catalog, method):
        self.catalog = catalog
        self.method = method

    def upload_catalog(self):
        tree = os.walk(self.catalog)
        for i in tree:
            variable = re.sub(r"\\", r"/", i[0])
            self.method.mkdir(variable)
            for file in i[2]:
                file1 = variable + "/" + file
                path = "/" + variable + "/" + file
                self.method.upload(file1, path)
        return "gj"

    def sum(self, a, b):
        return a + b

    def mult(self, a, b):
        return a * b
