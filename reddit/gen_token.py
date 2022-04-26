import requests


def run():
    # note that CLIENT_ID refers to 'personal use script' and SECRET_TOKEN to 'token'
    auth = requests.auth.HTTPBasicAuth(
        '', '')

    # here we pass our login method (password), username, and password
    data = {'grant_type': 'password',
            'username': '',
            'password': ''}

    # setup our header info, which gives reddit a brief description of our app
    headers = {'User-Agent': 'MyBot/0.0.1'}

    # send our request for an OAuth token
    res = requests.post('https://www.reddit.com/api/v1/access_token',
                        auth=auth, data=data, headers=headers)

    # convert response to JSON and pull access_token value
    TOKEN = res.json()['access_token']
    return TOKEN
