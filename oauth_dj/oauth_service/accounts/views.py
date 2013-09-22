# Create your views here.

from django.contrib.auth import login, logout, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render_to_response
from django.http import HttpResponseRedirect
from django.template import RequestContext

from accounts.forms import LoginForm


def login_page(request):
    if request.method == 'POST':
        redirect_to = request.REQUEST.get(REDIRECT_FIELD_NAME, '/')
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            login(request, login_form.get_user())
            print redirect_to
            return HttpResponseRedirect(redirect_to)
    login_form = LoginForm()
    return render_to_response("login_page.html", context_instance=RequestContext(
                request, {
                    "action": "login",
                    "form": login_form,
                    "errors": login_form.errors.values()
                }))


@login_required
def logout_page(request):
    logout(request)
    return redirect("/")
