#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.contrib.auth.models import User


def authenticate(email, password):
    try:
        user = User.objects.get(email=email)
    except:
        return None
    if user.check_password(password):
        user.backend = "django.contrib.auth.backends.ModelBackend"
        return user
    return None
