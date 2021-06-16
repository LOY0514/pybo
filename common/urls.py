# -*- coding: utf-8 -*-
"""
Created on Wed Jun 16 02:13:32 2021

@author: Admin
"""
from django.urls import path
from django.contrib.auth import views as auth_views

from . import views


app_name = 'common'

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='common/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('signup/', views.signup, name='signup'),
]