#!/usr/bin/env python
# -*- coding: utf-8 -*-

import urllib


CLIENT_ID = "1234567890"
REDIRECT_URI = "http://10.7.201.77:9000/accounts/index/"

LOGIN_URL = "http://10.7.201.77:8000/oauth2/authorize/?response_type=code&client_id=%s&redirect_uri=%s" % (
        CLIENT_ID, urllib.quote(REDIRECT_URI))
