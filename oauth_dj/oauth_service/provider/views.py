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
    response_type = request.REQUEST.get('response_type', None)
    client_id = request.REQUEST.get('client_id', None)
    redirect_uri = request.REQUEST.get('redirect_uri', None)

    try:
        client = Client.objects.get(client_id=client_id, redirect_uri=redirect_uri)
    except:
        return HttpResponseBadRequest("client id or redirect uri not matched")

    grant = Grant.objects.create(user=request.user, client=client, redirect_uri=redirect_uri)
    redirect_to = urlparse.urljoin(redirect_uri, "?code=" + grant.token)
    return HttpResponseRedirect(redirect_to)


def exchange_access_token(request):
    code = request.REQUEST.get('code', None)
    client_id = request.REQUEST.get('client_id', None)
    client_secret = request.REQUEST.get('client_secret', None)

    grants = Grant.objects.filter(token=code)
    if not grants.exists():
        return HttpResponseBadRequest("request error, code does not exist")
    clients =  Client.objects.filter(client_id=client_id, client_secret=client_secret)
    if not Client.objects.filter(client_id=client_id, client_secret=client_secret).exists():
        return HttpResponseBadRequest("client auth failed")

    access_token, create = AccessToken.objects.get_or_create(user=grants[0].user, client=clients[0])

    refresh_token, create = RefreshToken.objects.get_or_create(user=grants[0].user, client=clients[0], access_token=access_token)
    #rm the code
    grants.delete()
    return HttpResponse(json.dumps({
        "username": access_token.user.username,
        "access_token": access_token.token,
        "token_type": "read_books",
        "expires_in": datetime.strftime(access_token.expires, "%Y-%m-%d %X"),
        "refresh_token": refresh_token.token,
    }))


def get_related_book(request):
    if request.method == 'POST':
        access_token = request.POST.get("access_token")
        try:
            token_obj = AccessToken.objects.get(token=access_token)
        except:
            return HttpResponseBadRequest("access token auth failed")
        user = token_obj.user
        books = Book.objects.filter(users=user).values("title", "outline")
        return HttpResponse(json.dumps({
            "username": user.username,
            "books": list(books)
        }))
    else:
        return HttpResponseBadRequest("request method error, POST only")
