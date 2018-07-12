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
from MachLab.models import Userinfo, Model, Modelfile
from MachLab.settings import BASE_DIR
from MachLab.public import model_type_choices, icon_colors

# Login & Register & Logout #

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

# Account Settings #

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=16, widget=widgets.Input(attrs={'type':"username",'class':"form-control",'id':"exampleInputUsername",'readonly':True}))
    email = forms.EmailField(max_length=32, widget=widgets.EmailInput(attrs={'type':"email",'class':"form-control",'id':"exampleInputEmail"}))
    bio = forms.CharField(max_length=256, widget=widgets.Textarea(attrs={'class':"form-control"}), required=False)
    url = forms.URLField(max_length=256, widget=widgets.URLInput(attrs={'class':"form-control"}), required=False)
    location = forms.CharField(max_length=32, widget=widgets.Input(attrs={'class':"form-control"}), required=False)
    avatar = forms.ImageField(allow_empty_file=True)

    def set_initial_fields(self, user=None):
        if user:
            if user.username:
                self.fields['username'].initial = user.username
            if user.email:
                self.fields['email'].initial = user.email
            if user.userinfo:
                if user.userinfo.bio:
                    self.fields['bio'].initial = user.userinfo.bio
                if user.userinfo.url:
                    self.fields['url'].initial = user.userinfo.url
                if user.userinfo.location:
                    self.fields['location'].initial = user.userinfo.location
                if user.userinfo.avatar:
                    self.fields['avatar'].initial = user.userinfo.avatar

@login_required
def account_profile(request):
    context = {}
    context['title'] = '个人信息概览 | MachLab'
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        context['form'] = form
        avatar = request.FILES['avatar']
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            bio = cd['bio']
            url = cd['url']
            location = cd['location']
            try:
                user = User.objects.get(username=request.user.username)
                if request.user.username != username or request.user.email != email:
                    if username and email:
                        already_username = User.objects.get(username=username)
                        already_email = User.objects.filter(email=email).first()
                        if already_username or already_emails:
                            context['alreadyRegistered'] = True
                            return render(request, 'account-settings.html', context)
                        else:
                            user.email = email
                if user.userinfo:
                    if bio:
                        user.userinfo.bio = bio
                    if url:
                        user.userinfo.url = url
                    if location:
                        user.userinfo.location = location
                    if avatar:
                        user.userinfo.avatar = avatar
                user.userinfo.save()
                user.save()
            except Exception as e:
                context['updateInvalid'] = True
            finally:
                return render(request, 'account-settings.html', context)
    else:
        user = User.objects.get(username=request.user.username)
        form = ProfileForm()
        form.set_initial_fields(user)
        context['form'] = form
        return render(request, 'account-settings.html', context)
    
class AccountForm(forms.Form):
    oldpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput(attrs={'type':"password",'class':"form-control",'id':"exampleInputPassword"}))
    newpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput(attrs={'type':"password",'class':"form-control",'id':"exampleInputPassword"}))
    confirmpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput(attrs={'type':"password",'class':"form-control",'id':"exampleInputPassword"}))
 
@login_required
def account_password(request):
    context = {}
    context['title'] = '账户信息概览 | MachLab'
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    if request.method == 'POST':
        form = AccountForm(request.POST)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            oldpassword = cd['oldpassword']
            newpassword = cd['newpassword']
            confirmpassword = cd['confirmpassword']
            user = User.objects.get(username=request.user.get_username())

            if user.check_password(oldpassword):
                if newpassword == confirmpassword:
                    user.set_password(newpassword)
                    user.save()
                    auth.logout(request)
                    return HttpResponseRedirect('/')
                else:
                    context['oldPasswordWrong'] = True
            else:
                context['confirmPasswordWrong'] = True
            return render(request, 'password.html', context)
    else:
        context['form'] = AccountForm()
        return render(request, 'password.html', context)

def account_repositories(request):
    context = {}
    context['title'] = '个人模型概览 | MachLab'
    # User informtion #
    user = User.objects.get(username=request.user.username)

    # Models information #
    models = Model.objects.filter(user=user)
    for model in models:
        model.file_count = len(Modelfile.objects.filter(model=model))
    context['models'] = models
    return render(request, 'repositories.html', context)

def account_applications(request):
    context = {}
    context['title'] = '个人应用列表 | MachLab'
    apps = [{'name':'machlab', 'size':22},]
    context['apps'] = apps
    return render(request, 'applications.html', context)

# User Profile #

def user_profile(request, username=None):
    context = {}
    context['title'] = '用户概览 | MachLab'
    context['username'] = username
    tag = request.GET.get('tag')
    context['tag'] = tag

    # User informtion #
    user = User.objects.get(username=username)
    context['email'] = user.email
    if user.userinfo:
        context['bio'] = user.userinfo.bio
        context['url'] = user.userinfo.url
        context['location'] = user.userinfo.location
        context['avatar'] = user.userinfo.avatar

    # Models information #
    models = Model.objects.filter(user=user)
    for model in models:
        model.icon_color = icon_colors[model.model_type]
        model.model_type = model_type_choices[model.model_type][1]
    context['models'] = models
    return render(request, 'user-profile.html', context)