import zipfile
import os
import re


class Archive:
    def __init__(self, file):

        self.file = file

    def get_archive(self):

        self.path = os.path.abspath(self.file)

        self.zip_path = re.sub(r"(\..+)", r".zip", self.path)

        try:
            newzip = zipfile.ZipFile(self.zip_path, "w")
            newzip.write(self.file)
            newzip.close()
        except Exception:
            print("Что-то пошло не так...")
        print(re.sub(r"(\..+)", r".zip", self.file))

        return re.sub(r"(\..+)", r".zip", self.file)

    def get_archive_folder(self):

        self.path = os.path.abspath(self.file)
        newzip = zipfile.ZipFile(self.path + ".zip", "w")
        for folder, subfolders, files in os.walk(self.path):
            for file in files:
                newzip.write(
                    os.path.join(folder, file),
                    os.path.relpath(os.path.join(folder, file), self.path),
                    compress_type=zipfile.ZIP_DEFLATED,
                )

        newzip.close()

        return self.file + ".zip"

    def get_file(self):

        self.path = os.path.abspath(self.file)

        self.zip = zipfile.ZipFile(self.path)
        self.file_path = re.sub(r"(\..+)", r"", self.path)

        self.zip.extractall(self.file_path)
        self.zip.close()
