import requests
from flask import Flask, render_template, redirect,request
import webbrowser
import os

"""
easyauth

A pip library built to make OAuth2.0 authentication simple for scripting
"""

__version__ = "0.0.1"
__author__ = 'Dvyision'
__credits__ = 'Dvyision'


class oauth:
    AUTH_ENDPOINT = ''
    TOKEN_ENDPOINT = ''
    VALIDATION_ENDPOINT = ''
    CLIENT_ID = ''
    CLIENT_SECRET = ''
    REDIRECT_URI = ''
    SCOPES = []
    RESPONSE_TYPE = ""
    EXTRA_PARAMETERS = []
    BASIC_AUTH_USER = ''
    BASIC_AUTH_PWD = ''
    ACCESS_TOKEN = ''

    def __init__(self,AUTH_ENDPOINT,TOKEN_ENDPOINT,CLIENT_ID,CLIENT_SECRET,SCOPES,VALIDATION_ENDPOINT="",EXTRA_PARAMETERS=[],BASIC_AUTH_USER="",BASIC_AUTH_PWD=""):
        self.AUTH_ENDPOINT = AUTH_ENDPOINT
        self.TOKEN_ENDPOINT = TOKEN_ENDPOINT
        self.CLIENT_ID = CLIENT_ID
        self.CLIENT_SECRET = CLIENT_SECRET
        self.REDIRECT_URI = "http://localhost:5000/easyauth"
        self.SCOPES = '%20'.join(SCOPES)
        self.VALIDATION_ENDPOINT = VALIDATION_ENDPOINT
        self.EXTRA_PARAMETERS = '%20'.join(EXTRA_PARAMETERS)
        self.BASIC_AUTH_USER = BASIC_AUTH_USER
        self.BASIC_AUTH_PWD = BASIC_AUTH_PWD
        return

    def login(self):
        #build authorization url
        param_string = []
        param_string.append('client_id={}'.format(self.CLIENT_ID))
        #param_string.append('client_secret={}'.format(self.CLIENT_SECRET))
        param_string.append('redirect_uri={}'.format(self.REDIRECT_URI))
        param_string.append('scope={}'.format(self.SCOPES))
        param_string.append('response_type=code')
        if self.EXTRA_PARAMETERS != "":
            param_string.append(self.EXTRA_PARAMETERS)
        url = "{}?{}".format(self.AUTH_ENDPOINT, '&'.join(param_string))
        webbrowser.open(url)



        #start webserver to handle redirect
        app = Flask(__name__)

        @app.route('/easyauth', methods=['GET'])
        def cache():
            #get code from response
            code = request.args['code']

            #build token url
            param_string = []
            param_string.append('grant_type=authorization_code')
            param_string.append('code={}'.format(code))
            param_string.append('client_id={}'.format(self.CLIENT_ID))
            param_string.append('client_secret={}'.format(self.CLIENT_SECRET))
            param_string.append('redirect_uri={}'.format(self.REDIRECT_URI))
            response = requests.post('{}'.format(self.TOKEN_ENDPOINT),headers={'content-type':'application/x-www-form-urlencoded'},data='&'.join(param_string)).json()
            self.ACCESS_TOKEN = response['access_token']
            func = request.environ.get('werkzeug.server.shutdown')
            func()
            return "<title>EasyAuth</title><p>You can close this window now</p>"

        app.run(host="0.0.0.0", port=5000)

        os.system('cls' if os.name == 'nt' else 'clear')
        input("Logged In! Press Enter to continue...\r\n")

        #provide access token
        return self.ACCESS_TOKEN