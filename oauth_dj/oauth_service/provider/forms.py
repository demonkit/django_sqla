#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from accounts.utils import authenticate


class OauthLoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    response_type = forms.CharField(required=False, widget=forms.HiddenInput())
    client_id = forms.CharField(required=False, widget=forms.HiddenInput())
    redirect_uri = forms.CharField(required=False, widget=forms.HiddenInput())

    def __init__(self, *args, **kwargs):
        super(OauthLoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        self.user = authenticate(email, password)
        if not self.user or not self.user.is_active:
            raise forms.ValidationError("Wrong email or password")

        return self.cleaned_data

    def get_user(self):
        return self.user
