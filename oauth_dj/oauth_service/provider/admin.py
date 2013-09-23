#!/usr/bin/env python
# -*- coding: utf-8 -*-



from django.contrib import admin

from provider.models import Client, Grant, AccessToken, RefreshToken


class ClientAdmin(admin.ModelAdmin):
    pass


class GrantAdmin(admin.ModelAdmin):
    pass


class AccessTokenAdmin(admin.ModelAdmin):
    pass


class RefreshTokenAdmin(admin.ModelAdmin):
    pass


admin.site.register(Client, ClientAdmin)
admin.site.register(Grant, GrantAdmin)
admin.site.register(AccessToken, AccessTokenAdmin)
admin.site.register(RefreshToken, RefreshTokenAdmin)
