#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *

urlpatterns = patterns('provider.views',
    (r'^authorize', 'authorize'),
    (r'^login$', 'oauth_login'),
    (r'^accesstoken', 'exchange_access_token'),
    (r'^books/$', 'get_related_book'),
)

