import json
import urlparse
from datetime import datetime

from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render_to_response
from django.template import RequestContext

from books.models import Book
from provider.forms import OauthLoginForm
from provider.models import Client, Grant, AccessToken, RefreshToken


def oauth_login_required(func):
    def wrapper(request, *args, **kwargs):
        #check whether to require user login or not
        #check requested parameters, including client id exists
        if request.user.is_authenticated():
            return func(request, *args, **kwargs)
        else:
            response_type = request.REQUEST.get('response_type', None)
            client_id = request.REQUEST.get('client_id', None)
            redirect_uri = request.REQUEST.get('redirect_uri', None)
            login_form = OauthLoginForm()
            return render_to_response("oauth_login_page.html",
                   context_instance=RequestContext(request, {
                       'form': login_form
                    }))
    return wrapper


def oauth_login(request):
    if request.method == 'POST':
        login_form = OauthLoginForm(request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            return render_to_response("oauth_authorize.html",
                    context_instance=RequestContext(request, {
                        'form': login_form
                    }))
    return HttpResponseBadRequest("oauth login error, redo that")


@oauth_login_required
def authorize(request):
    if request.method == 'POST':
        response_type = request.POST.get('response_type', None)
        client_id = request.POST.get('client_id', None)
        redirect_uri = request.POST.get('redirect_uri', None)

        try:
            client = Client.objects.get(client_id=client_id, redirect_uri=redirect_uri)
        except:
            return HttpResponseBadRequest("client id or redirect uri not matched")

        grant, created = Grant.objects.get_or_create(user=request.user, client=client, redirect_uri=redirect_uri)
        redirect_to = urlparse.urljoin(redirect_uri, "?code=" + grant.token)
        return HttpResponseRedirect(redirect_to)
    else:
        return HttpResponseBadRequest("request method error, POST only")


def exchange_access_token(request):
    if request.method == 'POST':
        code = request.POST.get('code', None)
        client_id = request.POST.get('client_id', None)
        client_secret = request.POST.get('client_secret', None)

        grants = Grant.objects.filter(token=code)
        if not grants.exists():
            return HttpResponseBadRequest("request error, code does not exist")
        if Client.objects.filter(client_id=client_id, client_secret=client_secret):
            return HttpResponseBadRequest("client auth failed")

        access_token = AccessToken(user=grants[0].user, client_id=client_id)
        access_token.save()

        refresh_token = RefreshToken(user=grants[0].user, client_id=client_id, access_token=access_token)
        refresh_token.save()
        #rm the code
        grants.delete()
        return HttpResponse(json.dumps({
            "access_token": access_token.token,
            "token_type": "read_books",
            "expires_in": datetime.strftime(access_token.expires, "%Y-%m-%d %X"),
            "refresh_token": refresh_token.token,
        }))
    else:
        return HttpResponseBadRequest("request method error, POST only")


def get_related_book(request):
    if request.method == 'POST':
        access_token = request.POST.get("access_token")
        try:
            token_obj = AccessToken.objects.get(token=access_token)
        except:
            return HttpResponseBadRequest("access token auth failed")
        user = token_obj.user
        books = Book.objects.filter(user=user).values("title", "outline")
        return HttpResponse(json.dumps({
            "username": user.username,
            "books": books
        }))
    else:
        return HttpResponseBadRequest("request method error, POST only")
