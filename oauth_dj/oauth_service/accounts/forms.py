#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms
from django.contrib.auth.models import User

from accounts.utils import authenticate


class LoginForm(forms.Form):
    email = forms.EmailField(max_length=100)
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.user = None

    def clean(self):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")
        print email, password

        self.user = authenticate(email, password)
        if not self.user or not self.user.is_active:
            print self.user
            raise forms.ValidationError("Wrong email or password")

        return self.cleaned_data

    def get_user(self):
        return self.user
