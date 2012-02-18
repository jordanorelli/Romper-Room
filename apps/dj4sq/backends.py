from django.contrib.auth.backends import ModelBackend
from django.contrib.auth.models import User, check_password

class FoursquareAuthBackend(ModelBackend):
    def authenticate(self, oauth_token=None):
        if not oauth_token:
            return None
        try:
            return User.objects.get(foursquareuser__oauth_token=oauth_token)
        except User.DoesNotExist:
            return None
