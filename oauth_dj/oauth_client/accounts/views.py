# Create your views here.

from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render_to_response
from django.template import RequestContext

from accounts import conf
from accounts.models import Customer


def oauth2_login(request):
    return redirect(conf.LOGIN_URL)


def show_customer(request):
    uid = request.session.get('uid')
    if user is None:
        return login_with(request)
    try:
        customer = Customer.objects.get(pk=uid)
    except:
        return HttpResponseBadRequest("get logined user error")
    return render_to_response("show.html", context_instance=RequestContext(request, {
                "info": customer.customer_info,
                "access_token": customer.token
            }))


def index(request):
    return render_to_response("index.html")
