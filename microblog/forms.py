# -*- coding: utf-8 -*-
from microblog.models import *
from django import forms

class LoginForm(forms.Form):
    login = forms.CharField(label = 'Login')
    password = forms.CharField(widget = forms.PasswordInput(attrs={'size':10}), label = 'Senha')

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        widgets = {'password': forms.PasswordInput(attrs={'size':10})}

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        exclude = ('user','date')
