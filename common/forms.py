# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 03:02:23 2021

@author: Admin
"""

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")

    class Meta:
        model = User
        fields = ("username", "email")