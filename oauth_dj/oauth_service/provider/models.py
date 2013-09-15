from datetime import datetime, timedelta

from django.contrib.auth.models import User
from django.db import models

from provider.utils import gen_token


class Client(models.Model):
    user = models.ForeignKey(User, related_name="oauth2_client")
    name = models.CharField(max_length=200)
    url = models.CharField(max_length=200)
    redirect_uri = models.CharField(max_length=200)
    client_id = models.CharField(max_length=32)
    client_secret = models.CharField(max_length=32)
    client_type = models.CharField(max_length=20)

    def __unicode(self):
        return "%s %s" % (self.url, self.redirect_uri)


class Grant(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(Client)
    token = models.CharField(max_length=32)
    expires = models.DateTimeField()
    redirect_uri = models.CharField(max_length=200)
    scope = models.IntegerField(default=0)

    def __init__(self, *args, **kwargs):
        super(Grant, self).__init__(*args, **kwargs)
        self.token = gen_token(32)
        self.expires = datetime.now() + timedelta(days=15)

    def __unicode__(self):
        return self.token


class AccessToken(models.Model):
    user = models.ForeignKey(User)
    client = models.ForeignKey(Client)
    token = models.CharField(max_length=32)
    expires = models.DateTimeField()
    scope = models.IntegerField(default=2, choices=[2, 4, 6])

    def __unicode__(self):
        return self.token

    def __init__(self, *args, **kwargs):
        super(AccessToken, self).__init__(*args, **kwargs)
        self.token = gen_token(32)
        self.expires = datetime.now() + timedelta(days=15)
