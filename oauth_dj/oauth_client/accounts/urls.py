
from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    (r'^login$', 'oauth2_login'),
    (r'^callback', 'oauth2_callback'),
    (r'^index', 'index'),
    (r'^customer/', 'show_customer'),
)
