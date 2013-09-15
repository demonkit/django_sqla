import json
import urlparse
from datetime import datetime

from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from provider.forms import OauthLoginForm
from provider.models import Client, Grant, AccessToken


def oauth_login(request):
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return render_to_response("oauth_authorize.html")
    return HttpResponseBadRequest("oauth login method not allowed")


def authorize(request):
    response_type = request.REQUEST.get('response_type', None)
    client_id = request.REQUEST.get('client_id', None)
    redirect_uri = request.REQUEST.get('redirect_uri', None)

    if response_type is None or client_id is None or redirect_uri is None:
        return HttpResponseBadRequest("requested parameters missing")

    login_form = OauthLoginForm()
    return render_to_response("oauth_login_page.html", context_instance=RequestContext(
                request, {
                    "action": "oauth_login",
                    'client_id': client_id,
                    "form": login_form,
                    "errors": login_form.errors.values()
                }))


@login_required
def user_grant(request):
    if request.method == 'POST':
        grant_type = request.POST.get('grant_type', None)
        code = request.POST.get('code', None)
        client_id = request.REQUEST.get('client_id', None)
        redirect_uri = request.REQUEST.get('redirect_uri', None)
        if grant_type is not 'authorization_code' or code is None or redirect_uri is None:
            return HttpResponseBadRequest("requested parameters missing")
        try:
            client = Client.objects.get(client_id=client_id, token=code, redirect_uri=redirect_uri)
        except:
            return HttpResponseBadRequest("client id or redirect uri not matched")

        grant = Grant(user=request.user, client=client, redirect_uri=redirect_uri)
        grant.save()

        redirect_to = urlparse.urljoin(redirect_uri, "?code=" + grant.token)

        return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponseBadRequest("request method error, POST only")


def exchange_access_token(request):
    if request.method == 'POST':
        code = request.POST.get('code', None)
        client_id = request.POST.get('client_id', None)
        client_secret = request.POST.get('client_secret', None)
        try:
            client = Client.objects.get(client_id=client_id, client_secret=client_secret)
        except:
            return HttpResponseBadRequest("client auth failed")

        try:
            grant = Grant.objects.get(token=code, client=client)
        except:
            return HttpResponseBadRequest("client code not matched")

        access_token = AccessToken(user=grant.user, client=client)
        access_token.save()
        return HttpResponse(json.dumps({
            "access_token": access_token.token,
            "token_type": "read_books",
            "expires_in": datetime.strftime(access_token.expires, "%Y-%m-%d %X"),
            }))
    else:
        return HttpResponseBadRequest("request method error, POST only")
