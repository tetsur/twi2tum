from tumblpy import Tumblpy

CONSUMER_KEY = 'KhKTnhWK94XL2SOseVBWNSAQgwNYogPaPpvwHxkqoVcpX9KMKq'
CONSUMER_SECRET = 'uDxlYMpkLafTrHD4zUFIFW8UPiabvJFQRbMyd1EDKhZyeVRcxu'

t = Tumblpy(CONSUMER_KEY, CONSUMER_SECRET)

auth_props = t.get_authentication_tokens()
auth_url = auth_props['auth_url']

OAUTH_TOKEN = auth_props['oauth_token']
OAUTH_TOKEN_SECRET = auth_props['oauth_token_secret']

print(auth_url)
print(OAUTH_TOKEN)
print(OAUTH_TOKEN_SECRET)