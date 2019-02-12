import tweepy
import requests

consumer_key = 'aCVjJetrfW2fOZj3Pyo33sI5C'
consumer_secret = 'gpn8jyT3fgNNsX9AQnaTav5Hobc5NpmZT6KQGXXub0vuPEckYx'
access_token = '3109407644-zJUvsLDkzZXqZNVOC5EU1zlwWSq04F8sfpLjFrv'
access_token_secret = 'CZJ9AEbnwVPYbjnLd9S5sw1w2R5CqiIJXDglMy4D6DE0f'

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

def get_favs(user_name):
    favs = []
    fav_tweets = api.favorites(user_name)
    for tweet in fav_tweets:
        fav = {}
        fav["text"] = tweet.text
        if hasattr(tweet, "extended_entities"):
            images = []
            for media in tweet.extended_entities["media"]:
                images.append(media["media_url_https"])
            fav["images"] = images
        else:
            pass
        favs.append(fav)
    return favs

def post_tumblr(blog_host,favs):
    tumblr_post_endpoint = "https://api.tumblr.com/v2/blog/{blog_host}/post".format(blog_host=blog_host)
    for fav in favs:
        if fav.has_key("images"):
            image_urls = "\n".join(fav["images"])
            body = "<blockquote cite=\"{tweet_uri}\">{text}</blockquote>\n{image_urls}".format(tweet_uri=fav["tweet_uri"], text=fav["text"], image_urls=image_urls)
        else:
            body = "<blockquote cite=\"{tweet_uri}\">{text}</blockquote>".format(tweet_uri=fav["tweet_uri"], text=fav["text"])
    entry_data = {
        'body':body
    }
favs = get_favs("odenmis")
print(favs)