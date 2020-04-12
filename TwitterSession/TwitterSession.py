from requests_oauthlib import OAuth1Session
import pandas as pd
from itertools import chain

class TwitterSession:

    _client_id = None
    _client_secret = None
    _redirect_uri = None
    _request_token_url = None
    _authorization_url = None
    _access_token_url = None
    _session = None
    _token = None
    _followers_url = None

    def __init__(   self,
                    client_id,
                    client_secret,
                    redirect_uri='https://localhost',
                    request_token_url = 'https://api.twitter.com/oauth/request_token',
                    authorization_url = 'https://api.twitter.com/oauth/authorize',
                    access_token_url = 'https://api.twitter.com/oauth/access_token',
                    followers_url = 'https://api.twitter.com/1.1/followers/ids.json'):
        self._client_id = client_id
        self._client_secret = client_secret
        self._redirect_uri = redirect_uri
        self._request_token_url = request_token_url
        self._authorization_url = authorization_url
        self._access_token_url = access_token_url
        self._followers_url = followers_url

    def Authenticate(self):
        if((self._client_id != None) & (self._client_secret != None)):
            self._session = OAuth1Session(self._client_id, client_secret=self._client_secret)
            return(True)
        else:
            return (False)

    def GetAuthorizationUrl(self):
        self._session.fetch_request_token(self._request_token_url)
        authorization_url = self._session.authorization_url(self._authorization_url)
        return(authorization_url)

    def ConfirmAuthorizationWithUrl(self, url):
        self._session.parse_authorization_response(url)
        self._session.fetch_access_token(self._access_token_url)

    def _GetFollowersList(self, user_id, cursor = None, count = 500):
        if(cursor != None):
            params = {'user_id': user_id,
                      'cursor': cursor,
                      'count': count}
        else:
            params = {'user_id': user_id,
                      'count': count}

        r = self.Get(self._followers_url, params = params)

        if(r.status_code == 200):
            rList = [pd.DataFrame({'FollowerId': [follower]}) for follower in r.json()['ids']]
            if(r.json()['next_cursor'] != 0):
                rList = rList + self._GetFollowersList(user_id, r.json()['next_cursor'])
        else:
            rList = None
            print(r.json())

        return(rList)

    def GetFollowers(self, user_id, cursor = None, count = 500):
        rList = self._GetFollowersList(user_id = user_id, cursor = cursor, count = count)
        rValue = pd.concat(chain(rList))

        return(rValue)

    def Get(self, url, params = None):
        return(self._session.get(url, params = params))

    def Post(self, url, params = None):
        return(self._session.post(url, params = params))