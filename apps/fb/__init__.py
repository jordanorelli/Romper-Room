from django.conf import settings
from random import choice
from string import letters, digits
from django.contrib.auth.models import User
from requests import get
from urlparse import parse_qs
import json

auth_base_uri = 'https://www.facebook.com/dialog/oauth'
resource_base_uri = 'https://graph.facebook.com/'

def request_oauth_token(auth_code):
    uri = '%s%s' % (resource_base_uri, 'oauth/access_token')
    params = {
        'client_id': settings.FACEBOOK_APP_ID,
        'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
        'client_secret': settings.FACEBOOK_SECRET,
        'code': auth_code,
    }
    response = get(uri, params=params)
    token_info = parse_qs(response.content)
    print token_info
    # this is shite.  For some reason parse_qs returns these as lists
    return token_info['access_token'][0], int(token_info['expires'][0])

def get_self(oauth_token):
    uri = '%s%s' % (resource_base_uri, 'me')
    params = {'access_token': oauth_token}
    response = get(uri, params=params)
    if not response.ok:
        if response.errors:
            raise Exception(response.errors)
        raise Exception(response.content)
    return json.loads(response.content)

def create_base_user(raw):
    """Given a raw user response from the facebook API, creates, saves, and
    returns a corresponding local django.contrib.auth.models.User object."""
    try:
        return User.objects.get(email=raw['email'])
    except User.DoesNotExist:
        user = User(
            first_name=raw['first_name'],
            last_name=raw['last_name'],
            email=raw['email'],
            username=''.join([choice(letters+digits) for x in range(30)]),
        )
        user.save()
        return user
