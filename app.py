import tweepy
import pytumblr
import re
import os
import urllib.request
import urllib.error
import json

from flask import Flask, request
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
tum_blog_url = os.environ["ENV_TUM_BLOG_URL"]
tum_tags = os.environ["ENV_TUM_TAGS"]

tum_api = pytumblr.TumblrRestClient(tum_consumer_key, tum_consumer_secret,
                                    tum_oauth_token, tum_oauth_token_secret)


def get_latest_fav(tweet_id):
    fav = {}
    latest_fav_tweet = twi_api.get_status(tweet_id, tweet_mode='extended')
    latest_fav_tweet_text = re.sub(
        r'https://t.co/\w*', '', latest_fav_tweet.full_text)
    fav["text"] = latest_fav_tweet_text
    if hasattr(latest_fav_tweet, "extended_entities"):
        images = []
        for media in latest_fav_tweet.extended_entities["media"]:
            images.append(media["media_url_https"])
        fav["images"] = images
    else:
        pass
    tweet_author = latest_fav_tweet.user.screen_name
    fav["tweet_author"] = tweet_author
    fav["tweet_uri"] = "https://twitter.com/{tweet_author}/status/{tweet_id}".format(
        tweet_author=tweet_author, tweet_id=tweet_id)
    return fav


def post_tumblr(fav):
    if "images" in fav:
        img_paths = []
        # いったん画像を保存しないと複数枚投稿できない
        for i, url in enumerate(fav["images"]):
            ext = os.path.splitext(url)[1][:1]
            img_path = f'tmp_imgs/img_{i}.{ext}'
            download_file(url, img_path)
            img_paths.append(img_path)
        caption = "<blockquote><i>{text}</i></blockquote><br>from&nbsp;<a href=\"{tweet_uri}\">{tweet_author}&nbsp;on&nbsp;Twitter</a>".format(
            tweet_uri=fav["tweet_uri"], text=fav["text"], tweet_author=fav["tweet_author"])
        tags = []
        if tum_tags:
            tags = tum_tags.split(",")
        tum_api.create_photo(tum_blog_url, state="published", tags=tags
                             data=img_paths, caption=caption)
        # 投稿終わったら画像は削除する
        for img_path in img_paths:
            os.remove(img_path)
    else:
        tum_api.create_quote(tum_blog_url, state="published",
                             quote=fav["text"], source=f'from&nbsp;<a href=\"{fav["tweet_uri"]}\">{fav["tweet_author"]}&nbsp;on&nbsp;Twitter</a>')


def download_file(url, dst_path):
    try:
        with urllib.request.urlopen(url) as web_file:
            data = web_file.read()
            with open(dst_path, mode='wb') as local_file:
                local_file.write(data)
    except urllib.error.URLError as e:
        print(e)


@app.route("/")
def index():
    return 'Hello World!'


@app.route("/post", methods=['POST'])
def twi2tum():
    faved_tweet_link = json.loads(request.data)["linkToTweet"]
    expression = r"twitter.com/([^/]+)/status/([^/]+)"
    match = re.search(expression, faved_tweet_link)
    faved_tweet_id = match.group(2)
    latest_fav = get_latest_fav(faved_tweet_id)
    post_tumblr(latest_fav)
    return 'OK'


if __name__ == '__main__':
    app.run()
