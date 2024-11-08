from requests_oauthlib import OAuth1Session
from dotenv import load_dotenv
from bot import bot_response
import os, requests

load_dotenv()

consumer_key = os.getenv("CONSUMER_KEY")
consumer_secret = os.getenv("CONSUMER_SECRET")

access_token = os.getenv("ACCESS_TOKEN")
access_token_secret = os.getenv("ACCESS_TOKEN_SECRET")

oauth = OAuth1Session(
    consumer_key,
    client_secret=consumer_secret,
    resource_owner_key=access_token,
    resource_owner_secret=access_token_secret,
)

def tweet_media(media_url):
    image_response = requests.get(media_url)
    if image_response.status_code != 200:
        raise Exception("Failed to fetch the image from the media URL")
    upload_url = "https://upload.twitter.com/1.1/media/upload.json"
    files = {"media": image_response.content}
    upload_response = oauth.post(upload_url, files=files)
    if upload_response.status_code != 200:
        raise Exception(f"Media upload failed: {upload_response.json()}")
    media_id = upload_response.json().get("media_id_string")
    return media_id

def reply_to_tweet(tweet, id):
    media_url = bot_response(tweet)
    media_id = tweet_media(media_url)
    payload = {
        "text": "",
        "media": {"media_ids": [media_id]},
        "reply": {"in_reply_to_tweet_id": id},
    }
    response = oauth.post("https://api.twitter.com/2/tweets", json=payload)
    if response.status_code != 201:
        print(f"Error: {response.status_code}, {response.text}")
    else:
        message = response.json() if response.json() else "Successful"
        print(message)

