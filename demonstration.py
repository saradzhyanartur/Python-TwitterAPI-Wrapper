from twitter_caller import TwitterClient

API_KEY = 'Your API Key'
API_SECRET_KEY = 'Your API Secret Key'

DEV_ENV = 'Your Development Enviorment for premium endpoints'  #Optional argument for the TwitterClient class
#Reference: https://developer.twitter.com/en/docs/tweets/search/guides/premium-operators


client = TwitterClient(api_key = API_KEY, api_secret_key=API_SECRET_KEY, dev_env=DEV_ENV)
client.authenticate()

favorites = client.retreieve_favorites_list()
print(favorites)

tweets = client.retrieve_tweets_standard(
    q='AAPL',
    result_type='mixed',
    count=2
)

timeline = client.retrieve_user_timeline(
    screen_name = 'realDonaldTrump',
    count = 2
)

trends = client.retrieve_trends(
    id=2
)

tweets = client.retrieve_tweets_30day(
    query="AAPL",
    maxResults=100,
    fromDate=2020_06_15_00_00, #yyyy_mm_dd_hh_mm
    toDate=2020_06_16_00_00 #yyyy_mm_dd_hh_mm
)