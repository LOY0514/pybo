# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 00:06:32 2021

@author: Admin
"""

from django.urls import path

from . import views

app_name = 'pybo'


urlpatterns = [
    path('', views.index, name = 'index'),
    path('mypage/', views.mypage, name = 'mypage'),
    

    #question_id에 실제로 값을 저장해서 view.detail의 question_id 인수로 전달
    path('<int:question_id>/', views.detail, name = 'detail'),
    
    path('answer_create/<int:question_id>', views.answer_create, name='answer_create'), 
    
    path('question_create/', views.question_create, name='question_create'),
]