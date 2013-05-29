# -*- coding: utf-8 -*-

from django.conf import settings
from django.shortcuts import render_to_response

from models import Base, Language


def is_empty(request):
    session = request.db_session
    return len(session.query(Language).all()) <= 0


def populate(request):
    new_langs = [Language('Python','py'),Language('Ruby', 'rb'),
                Language('Common Lisp', 'lisp'),Language('Objective-C', 'm')]
    session.add_all(new_langs)
    session.commit()


def index(request):
    session = request.db_session
    if is_empty(request):
        populate(request)
    langs = session.query(Language).all()
    return render_to_response('with_sqlchemy.html',
            {'langs': langs})
