#!/usr/bin/env python
# -*- coding: utf-8 -*-


from django.contrib import admin

from books.models import Book, Author


class BookAdmin(admin.ModelAdmin):
    pass


class AuthorAdmin(admin.ModelAdmin):
    pass


admin.site.register(Book, BookAdmin)
admin.site.register(Author, AuthorAdmin)
