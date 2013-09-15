#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls.defaults import *

urlpatterns = patterns('books.views',
    (r'^$', 'index'),
    (r'^(?P<page_no>)\d+/(?P<num_per_page>\d+)$', 'index'),
)
