from django.conf.urls import patterns, include, url
from with_sqlalchemy import views
# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('django_sqla',
    (r'^$', views.index),
    # Examples:
    # url(r'^$', 'django_sqla.views.home', name='home'),
    # url(r'^django_sqla/', include('django_sqla.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
)
