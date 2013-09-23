from django.conf.urls import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', "books.views.index"),
    url(r'^book/', include("books.urls")),
    url(r'^accounts/', include("accounts.urls")),
    url(r'^oauth2/', include("provider.urls")),
)
