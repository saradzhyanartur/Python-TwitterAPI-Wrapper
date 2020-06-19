import urllib3
import base64
import json
import certifi
from urllib.parse import quote, urlencode
from typing import List, Optional, Dict, Union

from twitter_caller.errors import ClientPermissionError, StatusCodeError


class TwitterClient:
    """Responsible for handling interactions with Twitter's API.
    
    Attributes:
        api_key -- api key obtained from twitter
        api_secret_key -- api secret key obtained from twitter
        dev_env -- [optional] name of the development enviorment. Required for premium endpoints
    """

    http = urllib3.PoolManager(cert_reqs='CERT_REQUIRED', ca_certs=certifi.where())

    def __init__(self, api_key: str, api_secret_key: str, dev_env: Optional[str] = None) -> None:
        self.api_key = api_key
        self.api_secret_key = api_secret_key
        self.dev_env = dev_env


    def _set_auth_headers(self) -> bytes:
        """Private method that creates an authentication header. 
        Raises error if authentication function has not been called on the instance.
        Required on all endpoints.
        """
        reference = "https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0"

        if hasattr(self, '_token'):
            return {'Authorization': f'Bearer {self._token}'.encode('utf-8')}
        raise ClientPermissionError(message="The client has not been authenticated", 
                                            reference=reference)

    
    @staticmethod
    def _validate_premium_endpoint(dev_env: Union[str, None]) -> None:
        """Private static method that validates if the user has specified dev-env.
        Raises error if dev_env is not sepcified on the instance.
        Required on all premium endpoints.
        
        Attributes:
            dev_env -- name of the development enviorment
        """
        reference = "https://developer.twitter.com/en/docs/tweets/search/guides/premium-operators"

        if not dev_env:
            raise ClientPermissionError(message="This route can not be called without sepcifying development enviorment",
                                            reference=reference)


    def authenticate(self) -> None:
        """Public method that obtains an access token from Twitter's API and saves it as an instance variable.
        Must be executed before any endpoints can be accessed"""
        reference =  "https://developer.twitter.com/en/docs/basics/authentication/oauth-2-0"

        URL = "https://api.twitter.com/oauth2/token"
        basic_token = quote(self.api_key) + ':' + quote(self.api_secret_key)
        base64_basic_token = base64.b64encode(basic_token.encode('utf-8'))
        r = TwitterClient.http.request(
            method='POST',
            url = URL, 
            headers={
                'Authorization': b'Basic ' + base64_basic_token,
                'Content-Type': b'application/x-www-form-urlencoded;charset=UTF-8',
            },
            body=b'grant_type=client_credentials'
        )
        if r.status != 200:
            raise StatusCodeError(status_code = r.status, reference=reference,
                                        message="API Keys are not valid, unable to obtain access Bearer token")
        self._token = json.loads(r.data.decode('utf-8'))['access_token']


    def retrieve_tweets_30day(self, query: str, **kwargs) -> List:
        """Public method that returns data for the specified query and time period
        
        Parameters:
            query -- The equivalent of one premium rule/filter
        """
        reference = "https://developer.twitter.com/en/docs/tweets/search/api-reference/premium-search#DataEndpoint"

        TwitterClient._validate_premium_endpoint(dev_env = self.dev_env)
        URL = f"https://api.twitter.com/1.1/tweets/search/30day/{self.dev_env}.json"
        r = TwitterClient.http.request(
            method='GET',
            url = URL + '?' + urlencode({"query": query, **kwargs}), 
            headers=self._set_auth_headers()
        )
        if r.status != 200:
            raise StatusCodeError(status_code = r.status, reference=reference)
        return json.loads(r.data.decode('utf-8'))['results']


    def retrieve_tweets_standard(self, q: str, **kwargs) -> List:
        """Public method that returns a collection of relevant Tweets matching a specified query.

        Parameters:
            q -- A UTF-8, URL-encoded search query of 500 characters maximum
        """
        reference = "https://developer.twitter.com/en/docs/tweets/search/api-reference/get-search-tweets"

        URL = "https://api.twitter.com/1.1/search/tweets.json"
        r = TwitterClient.http.request(
            method='GET',
            url = URL + '?' + urlencode({'q': q, **kwargs}), 
            headers=self._set_auth_headers()
        )
        if r.status != 200:
            raise StatusCodeError(status_code = r.status, reference=reference)
        return json.loads(r.data.decode('utf-8'))["statuses"]


    def retrieve_trends(self, _id: int, **kwargs) -> List:
        """Public method that returns the top 50 trending topics.

        Parameters:
            _id -- The Yahoo! Where On Earth ID of the location to return trending information
                    IDs of location can be found at https://www.findmecity.com/
        """
        reference = "https://developer.twitter.com/en/docs/trends/trends-for-location/api-reference/get-trends-place"

        URL = "https://api.twitter.com/1.1/trends/place.json"
        r = TwitterClient.http.request(
            method='GET',
            url = URL + '?' + urlencode({'id': _id, **kwargs}), 
            headers=self._set_auth_headers()
        )
        if r.status != 200:
            raise StatusCodeError(status_code = r.status, reference=reference)
        return json.loads(r.data.decode('utf-8'))[0]["trends"]


    def retreieve_favorites_list(self, **kwargs):
        """Public method that returns the 20 most recent Tweets 
        liked by the authenticating or specified user."""
        reference = "https://developer.twitter.com/en/docs/tweets/post-and-engage/api-reference/get-favorites-list"

        URL = "https://api.twitter.com/1.1/favorites/list.json"
        r = TwitterClient.http.request(
            method='GET',
            url = URL + '?' +  urlencode({**kwargs}),
            headers=self._set_auth_headers()
        )
        if r.status != 200:
            raise StatusCodeError(status_code = r.status, reference=reference)
        return json.loads(r.data.decode('utf-8'))


