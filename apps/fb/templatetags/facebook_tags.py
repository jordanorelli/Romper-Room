from django.conf import settings
from django import template
from urllib import urlencode
from fb import auth_base_uri

register = template.Library()

auth_uri = '%s?%s' % (auth_base_uri, urlencode({
    'client_id': settings.FACEBOOK_APP_ID,
    'redirect_uri': settings.FACEBOOK_REDIRECT_URI,
    'scope': 'email',
}))

class AuthNode(template.Node):
    def render(self, context):
        return auth_uri

@register.tag
def facebook_auth_uri(parser, token):
    return AuthNode()
