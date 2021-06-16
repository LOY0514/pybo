# -*- coding: utf-8 -*-
"""
Created on Tue Jun 15 23:34:04 2021

@author: Admin
"""

from django import forms
from pybo.models import Question, Answer


class QuestionForm(forms.ModelForm):
    class Meta:
        model = Question
        fields = ['subject', 'content']
        
        
        widgets = {
            'subject': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 1}),
        }
        
        
        labels = {
            'subject': 'SwingName',
            'content': 'Type',
        }
        
class AnswerForm(forms.ModelForm):
    class Meta:
        model = Answer
        fields = ['content']
        labels = {
            'content': '답변내용',
        }