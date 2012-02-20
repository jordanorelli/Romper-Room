from datetime import datetime, timedelta
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.views.generic import View
from fb import request_oauth_token, get_self, create_base_user
from fb.models import FacebookUser

class OAuthReceiver(View):
    def get(self, request, *args, **kwargs):
        auth_code = request.GET.get('code')
        if not auth_code:
            # I'm just throwing out the error at the moment.  In a real-world
            # environment, I wouldn't do this.
            return HttpResponseRedirect('/')
        oauth_token, expires = request_oauth_token(auth_code)
        print oauth_token
        print expires
        raw = get_self(oauth_token)
        print repr(raw)

        try:
            user = User.objects.get(facebookuser__id=raw['id'])
            if user.facebookuser.oauth_token != oauth_token:
                user.facebookuser.oauth_token = oauth_token
                user.facebookuser.save()

        except User.DoesNotExist:
            user = create_base_user(raw)
            expiry = datetime.now() + timedelta(seconds=expires)
            facebook_user = FacebookUser(id=raw['id'], user=user,
                                         oauth_token=oauth_token,
                                         token_expiry=expiry)
            facebook_user.save()
        user = authenticate(oauth_token=oauth_token)
        login(request, user)
        return HttpResponseRedirect('/')
