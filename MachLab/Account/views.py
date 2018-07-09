# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.forms import widgets
from django.http import HttpResponse
from datetime import datetime
from MachLab.models import Userinfo
from MachLab.settings import BASE_DIR

class LoginForm(forms.Form):
    username = forms.CharField(max_length=16, widget=widgets.Input(attrs={'type':"username",'class':"form-control",'id':"exampleInputUsername"}))
    password = forms.CharField(max_length=16, min_length=6, widget=widgets.PasswordInput(attrs={'type':"password",'class':"form-control",'id':"exampleInputPassword"}))
    
    def clean_password(self):
        password = self.cleaned_data['password']
        password_length = len(password)
        if password_length < 6:
            raise forms.ValidationError("Not enough digits for password!")
        elif password_length > 16:
            raise forms.ValidationError("Too much digits for password!")
        return password

def login(request):
    context = {}
    context['title'] = '登录 | MachLab'
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = LoginForm(request.POST)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            password = cd['password']
            user = auth.authenticate(username=username, password=password)

            if user is not None:
                auth.login(request, user)
                request.session['username'] = username
                return HttpResponseRedirect(redirect_to)
            else:
                context['loginInvalid'] = True
                return render(request, 'login.html', context)
    else:
        context['form'] = LoginForm()
        return render(request, 'login.html', context)

class RegisterForm(forms.Form):
    email = forms.EmailField(max_length=32, widget=widgets.EmailInput(attrs={'type':"email",'class':"form-control",'id':"exampleInputEmail"}))
    username = forms.CharField(max_length=16,widget=widgets.Input(attrs={'type':"username",'class':"form-control",'id':"exampleInputUsername"}))
    password = forms.CharField(max_length=16, min_length=6, widget=widgets.PasswordInput(attrs={'type':"password",'class':"form-control",'id':"exampleInputPassword"}))
    
def register(request):
    context = {}
    context['title'] = '注册 | MachLab'
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            username = cd['username']
            password = cd['password']
            user = auth.authenticate(email=email, password=password)

            if user is not None:
                context['form'] = RegisterForm()
                context['alreadyRegistered'] = True
                return render(context, 'register.html', context)
            else:
                user = auth.authenticate(username=username, password=password)
                if user is not None:
                    context['form'] = RegisterForm()
                    context['alreadyRegistered'] = True
                    return render(context, 'register.html', context)
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    userinfo = Userinfo.objects.create(user=user, bio='', url='', location='', avatar=None)
                    userinfo.save()
                    auth.login(request, user)
                    return HttpResponseRedirect(redirect_to)
    else:
        context['form'] = RegisterForm()
        return render(request, 'register.html', context)

class LostPasswordForm(forms.Form):
    email = forms.EmailField(max_length=32, widget=widgets.EmailInput(attrs={'type':"email",'class':"form-control",'id':"exampleInputEmail"}))
    
#@csrf_exempt
def lost_password(request):
    context = {}
    context['title'] = '找回密码 | MachLab'
    if request.method == 'POST':
        form = LostPasswordForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
    else:
        form = LostPasswordForm()
        context['form'] = form
        return render(request, 'lost-password.html', context)
    
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')
