import os
from requests_oauthlib import OAuth1Session
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
import requests, os

load_dotenv()


from requests_oauthlib import OAuth1Session
import os
import json

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

request_token_url = "https://api.twitter.com/oauth/request_token?oauth_callback=oob"
oauth = OAuth1Session(consumer_key, client_secret=consumer_secret)

fetch_response = oauth.fetch_request_token(request_token_url)
resource_owner_key = fetch_response.get("oauth_token")
resource_owner_secret = fetch_response.get("oauth_token_secret")

base_authorization_url = "https://api.twitter.com/oauth/authorize"
authorization_url = oauth.authorization_url(base_authorization_url)
print("Please go here and authorize: %s" % authorization_url)
verifier = input("Paste the PIN here: ")

access_token_url = "https://api.twitter.com/oauth/access_token"
oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=resource_owner_key,
    resource_owner_secret=resource_owner_secret,
    verifier=verifier,
)
oauth_tokens = oauth.fetch_access_token(access_token_url)

access_token = oauth_tokens["oauth_token"]
access_token_secret = oauth_tokens["oauth_token_secret"]

print("Save these securely!")
print(f"Access Token: {access_token}")
print(f"Access Token Secret: {access_token_secret}")
