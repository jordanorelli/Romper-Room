from django.conf import settings
from django.contrib.auth.models import User
from requests import get
from urllib import urlencode
import json

auth_base_uri = 'https://foursquare.com/oauth2/'
resource_base_uri = 'https://api.foursquare.com/v2/'

def auth_uri(rel_uri):
    if rel_uri.startswith('/'):
        rel_uri = rel_uri[1:]
    return '%s%s' % (auth_base_uri, rel_uri)

def resource_uri(rel_uri):
    if rel_uri.startswith('/'):
        rel_uri = rel_uri[1:]
    return '%s%s' % (resource_base_uri, rel_uri)

def request_oauth_token(auth_code):
    params = {
        'client_id': settings.FOURSQUARE_CLIENT_ID,
        'client_secret': settings.FOURSQUARE_CLIENT_SECRET,
        'redirect_uri': settings.FOURSQUARE_REDIRECT_URI,
        'grant_type': 'authorization_code',
        'code': auth_code,
    }
    uri = auth_uri('access_token')
    response = get(uri, params=params)
    if not response.ok:
        raise Exception(response.error)
    response_dict = json.loads(response.content)
    return response_dict['access_token']

def get_self(oauth_token):
    """Given an oauth token, calls out to the foursquare API's users/self
    endpoint.  Returns a python object represeting the unmarshaled user data
    body of the json response."""
    uri = resource_uri('users/self')
    response = get(uri, params={'oauth_token': oauth_token})
    if not response.ok:
        raise Exception(response.content)
    body = json.loads(response.content)
    return body['response']['user']

def create_base_user(raw):
    """Given a raw user response from the foursquare API, creates, saves, and
    returns a corresponding local django.contrib.auth.models.User object."""
    user = User(
        first_name=raw['firstName'],
        last_name=raw['lastName'],
        email=raw['contact']['email'],
        username=raw['contact']['email'][:30],
    )
    user.save()
    return user
