from django.conf import settings
from django import template
register = template.Library()

class AuthNode(template.Node):
    def render(self, context):
        client_id = settings.FOURSQUARE_CLIENT_ID
        redirect_url = settings.FOURSQUARE_REDIRECT_URL
        return "https://foursquare.com/oauth2/authenticate?client_id=%s&response_type=code&redirect_uri=%s" % (client_id, redirect_url)

@register.tag
def foursquare_auth_uri(parser, token):
    return AuthNode()
