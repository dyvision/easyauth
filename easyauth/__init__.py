import requests
from flask import Flask, render_template, redirect,request
import webbrowser

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

    def __init__(self,AUTH_ENDPOINT,TOKEN_ENDPOINT,CLIENT_ID,CLIENT_SECRET,SCOPES,RESPONSE_TYPE="",VALIDATION_ENDPOINT="",EXTRA_PARAMETERS=[],BASIC_AUTH_USER="",BASIC_AUTH_PWD=""):
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
        self.RESPONSE_TYPE = RESPONSE_TYPE
        return

    def login(self):
        #build authorization url
        param_string = []
        param_string.append('client_id={}'.format(self.CLIENT_ID))
        #param_string.append('client_secret={}'.format(self.CLIENT_SECRET))
        param_string.append('redirect_uri={}'.format(self.REDIRECT_URI))
        param_string.append('scope={}'.format(self.SCOPES))
        if self.RESPONSE_TYPE != "":
            param_string.append('response_type={}'.format(self.RESPONSE_TYPE))
        if self.EXTRA_PARAMETERS != "":
            param_string.append(self.EXTRA_PARAMETERS)
        url = "{}?{}".format(self.AUTH_ENDPOINT, '&'.join(param_string))
        print(url)
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
            param_string.append('response_type=code')
            param_string.append('code={}'.format(code))
            param_string.append('client_id={}'.format(self.CLIENT_ID))
            param_string.append('client_secret={}'.format(self.CLIENT_SECRET))
            param_string.append('redirect_uri={}'.format(self.REDIRECT_URI))
            response = requests.post('{}'.format(self.TOKEN_ENDPOINT),headers={'content-type':'application/x-www-form-urlencoded'},data='&'.join(param_string)).json()
            self.ACCESS_TOKEN = response['access_token']
            func = request.environ.get('werkzeug.server.shutdown')
            func()
            return "You can close this window now"

        app.run(host="0.0.0.0", port=5000)

        input("Logged In! Press Enter to continue...")

        #provide access token
        return self.ACCESS_TOKEN


"""
    def authenticate(self,CODE):
        body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "authorization_code",
            "code": CODE,
            "scope": self.SCOPES,
            "redirect_uri": self.REDIRECT
        }

        result = requests.post(token_url, data=body).json()

        self.ACCESS_TOKEN = result['access_token']

        return result

    def refresh(self,REFRESH_TOKEN):
        body = {
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": REFRESH_TOKEN,
            "scope": self.SCOPES,
            "redirect_uri": self.REDIRECT
        }

        result = requests.post(token_url, data=body).json()

        self.ACCESS_TOKEN = result['access_token']

        return result
    
    def list(self,TABLE,QUERYSTRING=''):
        headers = {
            "Prefer": "odata.include-annotations=\"*\"",
            "content-type": "application/json; odata.metadata=full",
            "Authorization": "Bearer {}".format(self.ACCESS_TOKEN)
        }
        response = requests.get('https://{}/api/data/v9.0/{}{}'.format(self.TENANT,TABLE,QUERYSTRING), headers=headers).json()
        return response

    def get(self,TABLE,PRIMARY_ID):
        headers = {
            "Prefer": "odata.include-annotations=\"*\"",
            "content-type": "application/json; odata.metadata=full",
            "Authorization": "Bearer {}".format(self.ACCESS_TOKEN)
        }
        response = requests.get('https://{}/api/data/v9.0/{}({})'.format(self.TENANT,TABLE,PRIMARY_ID), headers=headers).json()
        return response

    def update(self,TABLE,PRIMARY_ID,BODY={}):
        headers = {
            "Prefer": "odata.include-annotations=\"*\"",
            "content-type": "application/json; odata.metadata=full",
            "Authorization": "Bearer {}".format(self.ACCESS_TOKEN)
        }
        try:
            response = requests.patch('https://{}/api/data/v9.0/{}({})'.format(self.TENANT,TABLE,PRIMARY_ID), headers=headers,json=BODY).json()
        except:
            response = {'code':'success','message':'updated {} record {}'.format(TABLE,PRIMARY_ID),'data':BODY}
        return response
    
    def create(self,TABLE,BODY={}):
        headers = {
            "Prefer": "odata.include-annotations=\"*\"",
            "content-type": "application/json; odata.metadata=full",
            "Authorization": "Bearer {}".format(self.ACCESS_TOKEN)
        }
        try:
            response = requests.post('https://{}/api/data/v9.0/{}'.format(self.TENANT,TABLE), headers=headers,json=BODY).json()
        except:
            response = {'code':'success','message':'created {} record'.format(TABLE),'data':BODY}
        return response

    def delete(self,TABLE,PRIMARY_ID):
        headers = {
            "Prefer": "odata.include-annotations=\"*\"",
            "content-type": "application/json; odata.metadata=full",
            "Authorization": "Bearer {}".format(self.ACCESS_TOKEN)
        }
        try:
            response = requests.delete('https://{}/api/data/v9.0/{}({})'.format(self.TENANT,TABLE,PRIMARY_ID), headers=headers).json()
        except:
            response = {'code':'success','message':'deleted {} record {}'.format(TABLE,PRIMARY_ID)}
        return response
        """