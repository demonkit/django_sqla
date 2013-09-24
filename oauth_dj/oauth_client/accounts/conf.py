#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib


CLIENT_ID = "1234567890"
CLIENT_SECRET = "1234567890"
REDIRECT_URI = "http://10.7.201.77:9000/accounts/callback/"

LOGIN_URL = "http://10.7.201.77:8000/oauth2/authorize/?response_type=code&client_id=%s&redirect_uri=%s" % (
        CLIENT_ID, urllib.quote(REDIRECT_URI))


OAUTH2_ACCESS_TOKEN_URL = "http://10.7.201.77:8000/oauth2/accesstoken/"

OAUTH2_GET_INFO_URL = "http://10.7.201.77:8000/oauth2/books/"
