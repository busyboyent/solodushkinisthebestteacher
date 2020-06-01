#!/usr/bin/env python
# coding: utf-8
from flask import *
import requests

client_id = "f7ceb48b6c624e91b404f16c01dd222d"
client_secret = "704f63962c9f4e03b1b1e5a18d880575"

app_key = "losy6b11rihhnj3"
app_secret = "9dq6mmlq1de9px3"

text = "Отлично! Теперь можете вернуться в консоль" + "и нажмите ctrl+c!"


class StartServer(object):
    def __init__(self):

        super(StartServer, self).__init__()
        self.start_server()

    def init_server(self):

        global client_id
        global client_secret

        global app_key
        global app_secret

        self.app = Flask(__name__)

        @self.app.route("/")
        def token():

            code = request.args.get("code")

            r = requests.post(
                "https://oauth.yandex.ru/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": client_id,
                    "client_secret": client_secret,
                },
            )

            j = json.loads(r.content)

            self.access_token = j["access_token"]

            return text

        @self.app.route("/dropbox", methods=["GET", ])
        def token_drop():

            code = request.args.get("code")

            r = requests.post(
                "https://api.dropboxapi.com/oauth2/token",
                data={
                    "grant_type": "authorization_code",
                    "code": code,
                    "client_id": app_key,
                    "client_secret": app_secret,
                    "redirect_uri": "http://localhost:8000/dropbox",
                },
            )

            j = json.loads(r.content)

            self.access_token = j["access_token"]

            return text

    def start_server(self):

        self.init_server()
        self.app.run(host="0.0.0.0", port=8000, debug=False)

    def get_token(self):

        return self.access_token
