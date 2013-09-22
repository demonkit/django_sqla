#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *

urlpatterns = patterns('provider.views',
    (r'authorize$', 'authorize'),
    (r'login$', 'oauth_login'),
)

