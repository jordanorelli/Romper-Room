from django.views.generic import TemplateView, View

class HomeView(TemplateView):
    def get_context_data(self, **kwargs):
        user = self.request.user
        context = {'params': kwargs}
        if user.is_authenticated():
            context.update({
                'foursquare_oauth_token': user.foursquareuser.oauth_token
            })
        return context

class ExploreView(View):
    pass
