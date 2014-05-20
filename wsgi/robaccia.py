#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os

import kid


extensions = {
    'html': 'text/html',
    'atom': 'application/atom+xml'
}


def render(start_response, template_file, vars):
    ext = template_file.rsplit('.')
    content_type = 'text/html'
    if len(ext) > 1 and (ext[1] in extensions):
        content_type = extensions[ext[1]]

    template = kid.Template(file=os.path.join('templates', template_file), **vars)
    body = template.serialize(encoding='utf-8')
    start_response("200 OK", [('Content-type', content_type)])
    return body
