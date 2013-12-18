#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.conf.urls import patterns, url, include
from django.views.generic import TemplateView

from books.views import AboutView


urlpatterns = patterns('',
    (r'^about/', AboutView.as_view()),
    (r'^about1/', TemplateView.as_view(template_name="about1.html")),
)
