from django.contrib.auth.models import User
from django.db import models

class FoursquareUser(models.Model):
    id = models.IntegerField(primary_key=True)
    user = models.OneToOneField(User)
    oauth_token = models.CharField(max_length=120)
