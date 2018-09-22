import constants
import oauth2

consumer = oauth2.Consumer(constants.CONSUMER_KEY, constants.CONSUMER_SECRET)
client = oauth2.Client(consumer)

client.request(constants.REQUEST_TOKEN_URL, 'POST')