#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    (r'^login/$', 'login_page'),
    (r'^logout/$', 'logout_page'),
)
