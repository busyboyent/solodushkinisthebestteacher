#!/usr/bin/env python
# coding: utf-8
from clint.textui import progress
from requests import request
import requests
import json


class YaDisk(object):

    url = "https://webdav.yandex.ru/"
    namespaces = {"d": "DAV:"}
    error_text = (
        "неправильно указан файл, проверьте его " +
        "наличие и обратитесь к help"
    )
    er_txt = "запрос не выполнен. проверьте токен и отправляемый запрос"

    def __init__(self, token):

        super(YaDisk, self).__init__()

        self.token = token

        if self.token is None:
            print(self.er_txt)

    def _sendRequest(self, type, addUrl="/", addHeaders={}, data=None):

        headers = {"Accept": "*/*"}
        headers.update(addHeaders)

        auth = {"Authorization": "OAuth " + self.token}
        headers.update(auth)

        url = self.url + addUrl
        return request(type, url, headers=headers, data=data)

    def ls(self, path=""):

        try:
            addUrl = ("https://cloud-api.yandex.net/v1/" +
                      "disk/resources?path=/" + path)

            auth = {"Authorization": "OAuth " + self.token}

            a = requests.get(addUrl, headers=auth)
            j = json.loads(a.content)

            for i in j["_embedded"]["items"]:
                print(i["name"])
        except Exception:
            print('убедитесь в корректности введеного пути')

    def mkdir(self, path):

        """ Создать каталог. Вся часть пути должна быть существующей"""

        resp = self._sendRequest("MKCOL", path)
        if resp.status_code != 201:

            print(self.er_txt)

    def remove(self, path):

        """Удалить файл или каталог."""

        resp = self._sendRequest("DELETE", path)

        if not (resp.status_code in (200, 204)):
            # raise YaDiskException(resp.status_code, resp.content)
            print(self.er_txt)

    def upload(self, file, path):

        """Загрузить файл"""
        try:
            with open(file, "rb") as f:
                addHeaders = {"Content-Type": "application/zip"}
                resp = self._sendRequest("PUT", path, data=f,
                                         addHeaders=addHeaders)
                if resp.status_code != 201:
                    print(self.er_txt)
        except Exception:
            print(self.error_text)

    def download(self, path, file):

        """Загрузите удаленный файл на диск."""
        addHeaders = {"Content-Type": "application/zip"}
        resp = self._sendRequest("GET", path, addHeaders=addHeaders)
        if resp.status_code == 200:
            with open(file, "wb") as f:
                total_length = int(resp.headers.get("content-length"))
                for chunk in progress.bar(
                    resp.iter_content(chunk_size=1024),
                    expected_size=(total_length / 1024) + 1,
                ):
                    if chunk:
                        f.write(chunk)
                        f.flush()
        else:
            # raise YaDiskException(resp.status_code, resp.content)
            print(self.er_txt)
