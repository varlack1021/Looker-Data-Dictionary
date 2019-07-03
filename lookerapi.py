import requests
import json
import urllib.request
import yaml
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)

host = 'localhost'


class LookerApi(object):

    def __init__(self, token, secret, host):

        self.token = token
        self.secret = secret
        self.host = host

        self.session = requests.Session()
        self.session.verify = False
        self.session.trust_env = False
        self.access_token = ""

        self.auth()

    def auth(self):
    url = '{}{}{}'.format(self.host, '/login?client_id=tNxzvyH7KxzXztnQ89z6&client_secret=',self.secret)
    params = {'client_id':self.token,
    'client_secret':self.secret}
    r = self.session.post(url)
    access = r.json().get('access_token')
    self.access_token = access
    #Sprint(access)



    head = {'Authorization': 'token {}'.format(access)}
    self.head = head
    self.session.headers.update(head)


    def get_model(self, model):
        url = '{}{}{}{}'.format(self.host, '/lookml_models/', model,'?access_token', self.access_token)
        look = self.session.get(url)
        if look.status_code == requests.codes.ok:
        return look.json() 


    def get_fields(self, model, explore, field):
        url = '{}{}{}{}{}'.format(self.host,'/lookml_models/', model, '/explores/', explore, '?access_token', self.access_token)
        r = self.session.get(url)
        if r.status_code == requests.codes.ok:
        return r.json()["fields"][field]



