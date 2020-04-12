from requests_oauthlib import OAuth2Session
import pandas as pd

class GoogleSession:

    _client_id = None
    _client_secret = None
    _redirect_uri = None
    _authorization_base_url = None
    _token_url = None
    _refresh_url = None
    _scope = None
    _session = None
    _token = None

    def __init__(   self,
                    client_id,
                    client_secret,
                    redirect_uri='https://localhost',
                    authorization_base_url='https://accounts.google.com/o/oauth2/v2/auth',
                    token_url='https://www.googleapis.com/oauth2/v4/token',
                    refresh_url='https://www.googleapis.com/oauth2/v4/token',
                    scope=[]):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._authorization_base_url = authorization_base_url
        self._token_url = token_url
        self._refresh_url = refresh_url
        self._scope = scope

    def Authenticate(self):
        if((self._client_id != None) & (self._scope != None) & (self._redirect_uri != None)):
            self._session = OAuth2Session(self._client_id, scope=self._scope, redirect_uri=self._redirect_uri)
            return(True)
        else:
            return (False)

    def GetAuthorizationUrl(self):
        authorization_url, state = self._session.authorization_url(authorization_base_url, access_type="offline", prompt="select_account")
        return(authorization_url)

    def ConfirmAuthorizationWithUrl(self, url):
        # Fetch the access token
        self._token = self._session.fetch_token(  token_url,
                                            client_secret=client_secret,
                                            authorization_response=url)

    def RefreshToken(self):
        self._session = OAuth2Session(  self._client_id,
                                        token=self._token,
                                        auto_refresh_kwargs=extra,
                                        auto_refresh_url=refresh_url,
                                        token_updater=self._token['refresh_token'])
        self._token = self._session.refresh_token(refresh_url)

    def Get(self, url, params = None):
        return(self._session.get(url, params = params))

    def Post(self, url, params = None):
        return(self._session.post(url, params = params))