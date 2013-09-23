#!/usr/bin/env python
# -*- coding: utf-8 -*-

import random


ALL_CHARACTERS_SET = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789'

def gen_token(length=32):
    return ''.join(random.sample(ALL_CHARACTERS_SET, length))
