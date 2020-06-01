#!/usr/bin/env python
# coding: utf-8
from initServer import *


client_id = "f7ceb48b6c624e91b404f16c01dd222d"
dropbox_id = "losy6b11rihhnj3"
redirect_uri = "http%3A%2F%2Flocalhost%3A8000%2Fdropbox"


class GetToken(object):
    def get_url_authorize(self):

        global client_id

        return (
            "https://oauth.yandex.ru/authorize?" +
            "response_type=code&client_id=" +
            client_id
        )

    def get_url_dropbox(self):

        global dropbox_id
        global redirect_uri

        return (
            "https://www.dropbox.com/oauth2/authorize?" +
            "response_type=code&client_id=" +
            dropbox_id +
            "&redirect_uri=" +
            redirect_uri
        )

    def get_token(self):

        self.server = StartServer()

        return self.server.get_token()
