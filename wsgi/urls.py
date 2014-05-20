#!/usr/bin/env python
# -*- coding: utf-8 -*-


import selector

import view


urls = selector.Selector()
urls.add('/blog/', GET=view.list)
urls.add('/blog/{id}', GET=view.member_get)
urls.add('/blog/;create_form', POST=view.create, GET=view.list)
urls.add('/blog/{id}/;edit_form', POST=view.member_update, GET=view.member_get)
