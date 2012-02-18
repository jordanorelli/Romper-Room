from dj4sq import request_oauth_token, create_base_user, get_self
from dj4sq.models import FoursquareUser
from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.views.generic import View
import json

class OAuthReceiver(View):
    """View responsible for implementing the server side of the OAuth
    "authorization code" flow (sometimes called the "web server flow").  This
    view must be on the receiving end of the callback URL registered at
    https://foursquare.com/oauth/consumer"""
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated():
            raise Exception("You're already logged in.")
        auth_code = request.GET['code']
        oauth_token = request_oauth_token(auth_code)
        try:
            User.objects.get(foursquareuser__oauth_token=oauth_token)
        except User.DoesNotExist:
            raw = get_self(oauth_token)
            user = create_base_user(raw)
            foursquare_user = FoursquareUser(id=raw['id'], user=user,
                                             oauth_token=oauth_token)
            foursquare_user.save()
        user = authenticate(oauth_token=oauth_token)
        login(request, user)
        return HttpResponseRedirect('/')
