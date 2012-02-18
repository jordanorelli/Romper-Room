from django.conf import settings
from django import template
from dj4sq import auth_base_uri
from urllib import urlencode
register = template.Library()

auth_uri = "%sauthenticate?%s" % (auth_base_uri, urlencode({
    'client_id': settings.FOURSQUARE_CLIENT_ID,
    'redirect_uri': settings.FOURSQUARE_REDIRECT_URI,
    'response_type': 'code',
}))

class AuthNode(template.Node):
    def render(self, context):
        return auth_uri

@register.tag
def foursquare_auth_uri(parser, token):
    return AuthNode()
