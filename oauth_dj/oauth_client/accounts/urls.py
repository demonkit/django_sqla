
from django.conf.urls.defaults import *

urlpatterns = patterns('accounts.views',
    (r'^login$', 'oauth2_login'),
    (r'^index', 'index'),
)
