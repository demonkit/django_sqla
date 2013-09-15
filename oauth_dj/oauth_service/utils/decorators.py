#!/usr/bin/env python
# -*- coding: utf-8 -*-


def check_user(func):
    def wrapper(request, *args, **kwargs):
        user = request.user
        return func(request, user, *args, **kwargs)
    return wrapper
