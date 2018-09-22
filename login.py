import constants
import oauth2
import urllib.parse as urlparse
import json

# create consumer, which uses key and secret to identify our app
consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

# use the client to perform a request for the request token
response, content = client.request(constants.REQUEST_TOKEN_URL, 'POST')
if response.status != 200:
  print("Error occured getting request token from Twitter!")

# get the request token parsing the query string returned
request_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

# ask the user to authorize our app and give us pin code
print("Go to the following site in your browser:")
print("{}?oauth_token={}".format(constants.AUTHORIZATION_URL, request_token['oauth_token']))

oauth_verifier = input("What's the pin? ")

# create a token object that contains the request token and the verifier
token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
token.set_verifier(oauth_verifier) #sets the secret and adds together


# create a client with our consumer (our app) and new created (and verified) token
client = oauth2.Client(consumer, token)

# ask Twitter for an access token, and Twitter knows bc we verified the req token
response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST') # content var gets overwritten
access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))

print(access_token)

# create an 'authenticated_token' token obj and use that to perform twitter api calls on behalf of user
authorized_token = oauth2.Token(access_token['oauth_token'], access_token['oauth_token_secret'])
authorized_client = oauth2.Client(consumer, authorized_token)

# make twitter api calls
response, content = authorized_client.request('https://api.twitter.com/1.1/search/tweets.json?q=javascript', 'GET')
if response.status != 200:
  print("An error occured while searching!")

tweets = json.loads(content.decode('utf-8'))

for tweet in tweets['statuses']:
  print(tweet['text'])

