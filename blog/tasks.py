import requests


# Send a post to Facebook page using Facebook Graph API Access Token with Python
#Your Access Keys
# https://developers.facebook.com/docs/pages/publishing/?locale=es_ES
# https://medium.com/nerd-for-tech/automate-facebook-posts-with-python-and-facebook-graph-api-858a03d2b142
page_id_1 = 123456789
facebook_access_token_1 = 'paste-your-page-access-token-here'
msg = 'Purple Ombre Bob Lace Wig Natural Human Hair now available on https://lace-wigs.co.za/'
photo_url = 'path to photo'
post_url = 'https://graph.facebook.com/{}/feed'.format(page_id_1)
payload = {
'message': msg,
'url': photo_url,
'access_token': facebook_access_token_1
}r = requests.post(post_url, data=payload)
print(r.text)
