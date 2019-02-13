import tweepy
from tumblpy import Tumblpy
import re
import os

from flask import Flask
app = Flask(__name__)

twi_consumer_key = os.environ["ENV_TWI_CONSUMER_KEY"]
twi_consumer_secret = os.environ["ENV_TWI_CONSUMER_KEY_SECRET"]
twi_access_token = os.environ["ENV_TWI_ACCESS_TOKEN"]
twi_access_token_secret = os.environ["ENV_TWI_ACCESS_TOKEN_SECRET"]

twi_auth = tweepy.OAuthHandler(twi_consumer_key, twi_consumer_secret)
twi_auth.set_access_token(twi_access_token, twi_access_token_secret)

twi_api = tweepy.API(twi_auth)

tum_consumer_key = os.environ["ENV_TUM_CONSUMER_KEY"]
tum_consumer_secret = os.environ["ENV_TUM_CONSUMER_KEY_SECRET"]
tum_oauth_token = os.environ["ENV_TUM_OAUTH_TOKEN"]
tum_oauth_token_secret = os.environ["ENV_TUM_OAUTH_TOKEN_SECRET"]

tum_api = Tumblpy(tum_consumer_key, tum_consumer_secret, tum_oauth_token, tum_oauth_token_secret)

def get_latest_fav(user_name):
    fav = {}
    latest_fav_tweet = twi_api.favorites(user_name)[0]
    latest_fav_tweet_text = re.sub(r'https://t.co/\w*','',latest_fav_tweet.text)
    fav["text"] = latest_fav_tweet_text
    if hasattr(latest_fav_tweet, "extended_entities"):
        images = []
        for media in latest_fav_tweet.extended_entities["media"]:
            images.append(media["media_url_https"])
        fav["images"] = images
    else:
        pass
    tweet_id = latest_fav_tweet.id
    tweet_author = latest_fav_tweet.user.screen_name
    fav["tweet_author"] = tweet_author
    fav["tweet_uri"] = "https://twitter.com/{tweet_author}/status/{tweet_id}".format(tweet_author=tweet_author, tweet_id=tweet_id)
    return fav

def post_tumblr(blog_url,fav):
    if "images" in fav:
        image_urls = ""
        for url in fav["images"]:
            url_for_post = "<img src=\"{url}\">".format(url=url)
            image_urls += url_for_post
        body = "<i>{text}</i>\n\n<image>{image_urls}</image>\n\nfrom&nbsp;<a href=\"{tweet_uri}\">{tweet_author}&nbsp;on&nbsp;Twitter</a>".format(tweet_uri=fav["tweet_uri"], text=fav["text"], image_urls=image_urls, tweet_author=fav["tweet_author"])
    else:
        body = "<i>{text}</i>from&nbsp;<a href=\"{tweet_uri}\">{tweet_author}&nbsp;on&nbsp;Twitter</a>".format(tweet_uri=fav["tweet_uri"], text=fav["text"], tweet_author=fav["tweet_author"])
    entry_data = {
        'body':body
    }
    tum_api.post('post', blog_url=blog_url, params=entry_data)

@app.route("/", methods=['GET'])
def twi2tum():
    latest_fav = get_latest_fav("odenmis")
    blog_url = "tetsunoaka.tumblr.com"
    post_tumblr(blog_url, latest_fav)
if __name__ == '__main__':
    app.run()