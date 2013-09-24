# Create your views here.

import json
import urllib
import urllib2

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from accounts import conf
from accounts.models import Customer


def oauth2_login(request):
    return redirect(conf.LOGIN_URL)


def oauth2_callback(request):
    data = {
        'code': request.REQUEST.get("code"),
        'client_id': conf.CLIENT_ID,
        'client_secret': conf.CLIENT_SECRET
    }
    data=urllib.urlencode(data)
    req = urllib2.Request(conf.OAUTH2_ACCESS_TOKEN_URL, data=data)
    resp = urllib2.urlopen(req)
    result = json.loads(resp.read())
    customer, create = Customer.objects.get_or_create(username=result['username'],
                        token=result['access_token'],
                        refresh_token=result['refresh_token'],
                        expireds=result['expires_in'],
                )
    customer.save()
    return redirect("/accounts/customer/?id=" + str(customer.pk))


def show_customer(request):
    uid = request.REQUEST.get('id')
    try:
        customer = Customer.objects.get(pk=uid)
    except:
        return HttpResponseBadRequest("get logined user error")
    req = urllib2.Request(conf.OAUTH2_GET_INFO_URL,
            data=urllib.urlencode({
                "access_token": customer.token
            }))
    resp = urllib2.urlopen(req)
    result = resp.read()
    result = json.loads(result)
    customer.customer_info = result
    customer.save()
    return render_to_response("show.html", context_instance=RequestContext(request, {
                "info": customer.customer_info,
                "access_token": customer.token
            }))


def index(request):
    return render_to_response("index.html")
