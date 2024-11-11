from tweet import reply_to_tweet
from dotenv import load_dotenv
import os, re, time
import requests

load_dotenv()

USER_ID = os.getenv("TWITTER_USER_ID")
BEARER_TOKEN = os.getenv("TWITTER_BEARER_TOKEN")
LAST_PROCESSED_ID = None

def fetch_mentions(last_processed_id):
    url = f"https://api.twitter.com/2/users/{USER_ID}/mentions"
    headers = {"Authorization": f"Bearer {BEARER_TOKEN}"}
    params = {
        "since_id": last_processed_id,
        "expansions": "author_id",
        "user.fields": "username",
        "max_results": 5
    } if last_processed_id else {
        "expansions": "author_id",
        "user.fields": "username",
        "max_results": 5
    }
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    return data

def get_newest_tweet(data):
    data = [tweet for tweet in data["data"] if tweet["author_id"] != USER_ID]
    return None if not data else max(data, key=lambda tweet: tweet["id"])

def get_cleaned_text(tweet):
    text = tweet.get("text", "")
    cleaned_text = re.sub(r"@\w+", "", text).strip()
    return cleaned_text

def run_eve():
    with open("file.txt", "r") as f: last_id = f.read().strip()
    data = fetch_mentions(last_id)
    # print(data)
    if 'data' in data:
        tweet = get_newest_tweet(data)
        if tweet:
            print(tweet)
            content = get_cleaned_text(tweet)
            response = reply_to_tweet(content, tweet.get('id'))
            with open("file.txt", "w") as f: f.write(tweet.get('id'))
            print(response)
        else:
            print("Nothing")
    print("====================Sleeping 15mins====================")
    time.sleep(900)
    
run_eve()
