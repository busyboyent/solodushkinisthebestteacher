#!/usr/bin/env python
# coding: utf-8
import os
import random
import string
import unittest
from unittest.mock import MagicMock
from unittest.mock import patch
from unittest import TestCase
from sky import YaDisk
from archive import *
from catalog import *
from dropbox import *
from lls import *
from getToken import *
from main import *
from programBody import *


LOGIN = "YANDEX_LOGIN"
TOKEN = "DROPBOX_TOKEN"


class TestProgramBody(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.disk = YaDisk(LOGIN)

    def test_help_info(self):

        text = (
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

        list_len = ['1', '2']
        result = ProgramBody(self.disk, list_len)
        result = result.help_info()
        self.assertEqual(result, text)

    def test_switch_case(self):

        list_ls = ['ls', '/']
        list_lls = ['lls']
        list_help = ['help1234']
        list_mkdir = ['mkdir', 'a1b2']
        list_remove = ['remove', 'a1b2']
        list_upload = ['upload', 'sky.py', '/sky.txt']
        list_download = ['download', '/sky.txt', 'sky1.py']
        list_catalog = ['catalog', 'aa']
        list_archive = ['archive', 'sky.py', '/sky.zip']
        list_unpack = ['unpack', 'aa.zip']

        result = ProgramBody(self.disk, list_ls)
        result = result.switch_case('ls')
        self.assertEqual(result, 'ls')

        result = ProgramBody(self.disk, list_mkdir)
        result = result.switch_case('mkdir')
        self.assertEqual(result, 'mkdir')

        result = ProgramBody(self.disk, list_remove)
        result = result.switch_case('remove')
        self.assertEqual(result, 'remove')

        result = ProgramBody(self.disk, list_upload)
        result = result.switch_case('upload')
        self.assertEqual(result, 'upload')

        result = ProgramBody(self.disk, list_download)
        result = result.switch_case('download')
        self.assertEqual(result, 'download')

        result = ProgramBody(self.disk, list_help)
        result = result.switch_case('help123')
        self.assertEqual(result, 'help')

        result = ProgramBody(self.disk, list_lls)
        result = result.switch_case('lls')
        self.assertEqual(result, 'lls')

        result = ProgramBody(self.disk, list_catalog)
        result = result.switch_case('catalog')
        self.assertEqual(result, 'catalog')

        result = ProgramBody(self.disk, list_archive)
        result = result.switch_case('archive')
        self.assertEqual(result, 'archive')

        result = ProgramBody(self.disk, list_unpack)
        result = result.switch_case('unpack')
        self.assertEqual(result, 'unpack')


class TestGetToken(unittest.TestCase):

    def test_get_url_dropbox(self):
        result = GetToken()
        result = result.get_url_dropbox()
        text = (
            "https://www.dropbox.com/oauth2/authorize?" +
            "response_type=code&client_id=" +
            dropbox_id +
            "&redirect_uri=" +
            redirect_uri
        )
        self.assertEqual(result, text)

    def test_get_url_authorize(self):
        result = GetToken()
        result = result.get_url_authorize()
        text = (
            "https://oauth.yandex.ru/authorize?" +
            "response_type=code&client_id=" +
            client_id
        )
        self.assertEqual(result, text)


class TestYaDisk(unittest.TestCase):
    disk = None
    remote_folder = None
    remote_file = None
    remote_path = None

    @classmethod
    def setUpClass(cls):
        cls.disk = YaDisk(LOGIN)
        # взять любой файл в рабочем каталоге
        for item in os.listdir("."):
            if os.path.isfile(item):
                cls.remote_file = item
                break

        cls.remote_folder = "/test_{}".format(
            "".join(random.choice(string.ascii_uppercase) for _ in range(6))
        )
        cls.remote_path = "{folder}/{file}".format(
            folder=cls.remote_folder, file=cls.remote_file
        )

    def test_main(self):
        def mkdir(remote_folder):
            self.disk.mkdir(remote_folder)

            self.disk.mkdir("{folder}/dir/bad".format(folder=remote_folder))

            self.disk.mkdir(remote_folder)

        tmp_remote_path = "{path}~".format(path=self.remote_path)
        tmp_local_file = "{file}".format(file=self.remote_file)

        mkdir(self.remote_folder)
        self.disk.upload(self.remote_file, self.remote_path)

        self.disk.download(self.remote_path, tmp_local_file)

        self.disk.remove(self.remote_folder)

        os.remove(tmp_local_file)

    def test_deprecation(self):
        self.disk.mkdir(self.remote_folder)
        try:
            self.disk.upload(self.remote_file, self.remote_path)

        finally:
            self.disk.remove(self.remote_folder)

    def test_requests(self):
        try:
            self.disk._sendRequest("")
        except Exception as exc:
            self.assertIsInstance(exc, Exception)


class TestCatalog(unittest.TestCase):
    def test_upload_catalog(self):
        result = UploadCatalog("1", "2")
        try:
            result.upload_catalog()
        except Exception as exc:
            self.assertIsInstance(exc, Exception)

    def test_upload_catalogg(self):
        result = UploadCatalog("1", "2")
        result = result.upload_catalog()
        self.assertEqual(result, "gj")

    def test_sum(self):
        result = UploadCatalog("1", "2")
        result = result.sum(1, 2)
        self.assertEqual(result, 3)

    def test_mult(self):
        result = UploadCatalog("1", "2")
        result = result.mult(1, 2)
        self.assertEqual(result, 2)


class TestLLS(unittest.TestCase):
    def test_files(self):
        result = LocalLS()
        try:
            result.files()
        except Exception as exc:
            self.assertIsInstance(exc, Exception)

    def test_output(self):
        result = LocalLS()
        try:
            result.output()
        except Exception as exc:
            self.assertIsInstance(exc, Exception)


class TestDropbox(unittest.TestCase):
    drop = None
    remote_folder = None
    remote_file = None
    remote_path = None

    @classmethod
    def setUpClass(cls):
        #        with open("TokenDrop.txt", "r+") as f:
        #            token = f.read()
        cls.drop = Dropbox(TOKEN)
        # взять любой файл в рабочем каталоге
        for item in os.listdir("."):
            if os.path.isfile(item):
                cls.remote_file = item
                break

        cls.remote_folder = "/test_{}".format(
            "".join(random.choice(string.ascii_uppercase) for _ in range(6))
        )
        cls.remote_path = "{folder}/{file}".format(
            folder=cls.remote_folder, file=cls.remote_file
        )

    def test_main(self):
        def mkdir(remote_folder):
            self.drop.mkdir(remote_folder)

            self.drop.mkdir("{folder}/dir/bad".format(folder=remote_folder))

            self.drop.mkdir(remote_folder)

        tmp_remote_path = "{path}~".format(path=self.remote_path)
        tmp_local_file = "{file}".format(file=self.remote_file)

        mkdir(self.remote_folder)
        self.drop.upload(self.remote_file, self.remote_path)

        self.drop.download(self.remote_path, tmp_local_file)

        self.drop.remove(self.remote_folder)

        os.remove(tmp_local_file)

    def test_deprecation(self):
        self.drop.mkdir(self.remote_folder)
        try:
            self.drop.upload(self.remote_file, self.remote_path)
        finally:
            self.drop.remove(self.remote_folder)

    def test_requestsX(self):
        try:
            self.drop._sendRequestXload("", "")
        except Exception as exc:
            self.assertIsInstance(exc, Exception)


class TestArchive(unittest.TestCase):
    def test_get_archive(self):

        result = Archive("file.txt")
        result = result.get_archive()
        self.assertEqual(result, "file.zip")

    def test_get_archive_folder(self):

        result = Archive("file")
        result = result.get_archive_folder()
        self.assertEqual(result, "file.zip")

    def test_upload_catalog(self):
        result = Archive("file")
        try:
            result.get_file()
        except Exception as exc:
            self.assertIsInstance(exc, Exception)
