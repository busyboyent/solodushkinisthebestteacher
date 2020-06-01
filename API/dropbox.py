#!/usr/bin/python
import requests
from requests import request
import json
from text import *
import os


class Dropbox:

    url = "https://api.dropboxapi.com/2/"
    add_url_req = "file_requests/"
    add_url_prop = "file_properties/properties/"
    error_text = (
        "неправильно указан файл, проверьте его " +
        "наличие и обратитесь к help"
    )
    er_txt = "запрос не выполнен. проверьте токен и отправляемый запрос"
    text = Text()

    def __init__(self, token):

        super(Dropbox, self).__init__()

        self.token = token

        if self.token is None:

            print("Пожалуйста, авторизируйте токен")

    def _sendRequest(self, addUrl="/", data=None):

        headers = {
            "Authorization": "Bearer " + self.token,
            "Content-Type": "application/json",
        }
        url = self.url + addUrl
        return requests.post(url, headers=headers, data=json.dumps(data))

    def _sendRequestXload(self, addUrl, path, addHeaders={}, data=None):

        headers = {
            "Authorization": "Bearer " + self.token,
            "Dropbox-API-Arg": '{"path":"' + path + '"}',
        }
        headers.update(addHeaders)
        url = addUrl
        return requests.post(url, headers=headers, data=data)

    def ls(self, path=""):

        addUrl = "files/list_folder"
        data = {"path": path}
        a = self._sendRequest(addUrl, data=data)
        j = json.loads(a.content)

        for i in j["entries"]:
            print(i["name"])

    def download(self, path, file):

        """Загрузите удаленный файл на диск."""
        addHeaders = {"Content-Type": "application/zip"}
        addUrl = "https://content.dropboxapi.com/2/files/download"
        resp = self._sendRequestXload(addUrl, path)

        if resp.status_code == 200:
            with open(file, "wb") as f:
                f.write(resp.content)
        else:
            print(self.er_txt)

    def upload(self, file, path):

        addUrl = "https://content.dropboxapi.com/2/files/upload"
        addHeaders = {"Content-Type": "application/octet-stream"}

        try:
            with open(file, "rb") as f:
                resp = self._sendRequestXload(
                    addUrl, path, addHeaders=addHeaders, data=f
                )

                if resp.status_code != 200:
                    print(self.er_txt)
        except Exception:
            print(self.error_text)

    #    def upload(self, file, path):
    #
    # url_start =
    # "https://content.dropboxapi.com/2/files/upload_session/start"
    # url_append =
    # "https://content.dropboxapi.com/2/files/upload_session/append_v2"
    # url_finish =
    # "https://content.dropboxapi.com/2/files/upload_session/finish"
    #
    #        addHeaders = {"Content-Type": "application/octet-stream"}
    #
    #        with open(file, "rb") as f:
    #
    #            file_size = os.path.getsize(file)
    #            chunk_size = 4 * 1024 * 1024
    #
    #            if file_size <= chunk_size:
    #                self.upload1(file, path)
    #            else:
    #                pass

    def mkdir(self, path):

        """ Создать каталог. Вся часть пути должна быть существующей"""
        addUrl = "files/create_folder_v2"
        data = {"path": "/" + path}
        resp = self._sendRequest(addUrl, data)

        if resp.status_code != 200:
            print(self.er_txt)

    def remove(self, path):

        """Удалить файл или каталог."""
        addUrl = "files/delete_v2"
        data = {"path": "/" + path}
        resp = self._sendRequest(addUrl, data)

        if not (resp.status_code in (200, 204)):
            print(self.er_txt)
