from tumblpy import Tumblpy

CONSUMER_KEY = 'KhKTnhWK94XL2SOseVBWNSAQgwNYogPaPpvwHxkqoVcpX9KMKq'
CONSUMER_SECRET = 'uDxlYMpkLafTrHD4zUFIFW8UPiabvJFQRbMyd1EDKhZyeVRcxu'
OAUTH_TOKEN = 'HD0KVRg4FLKIvleyGMkqz8ltUdJHO1uWT3ppmpZhUBafxA4OuZ'
OAUTH_TOKEN_SECRET = 'sUzvI1gZz9YMzxbmXfGIyV41OyBtDnkI35im95ugrnZpHSXssR'

t = Tumblpy(CONSUMER_KEY, CONSUMER_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)

oauth_verifier = '5JGiy43HZSx4c1TLgBpf2eN1OtJMmiSHAu9B4HdqJNxQRxT8y3'
authorized_tokens = t.get_authorized_tokens(oauth_verifier)

oauth_token = authorized_tokens['oauth_token']
oauth_token_secret = authorized_tokens['oauth_token_secret']

print(oauth_token)
print(oauth_token_secret)