# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib import auth
from django.contrib.auth.models import User
#from MachLab.models import MyUser, MyUserManager
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=16)
    email = forms.EmailField(max_length=32)
    bio = forms.CharField(max_length=256)
    url = forms.URLField(max_length=256)
    location = forms.CharField(max_length=32)
    avatar = forms.ImageField()

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
def profile(request):
    context = {}
    context['title'] = '个人信息概览 | MachLab'
    redirect_to = request.POST.get('next')
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        context['form'] = form
        if form.is_valid():
            cd = form.cleaned_data
            username = cd['username']
            email = cd['email']
            bio = cd['bio']
            url = cd['url']
            location = cd['location']
            avatar = cd['avatar']
            try:
                user = User.objects.get(username=request.user.username)
                if username:
                    user.username = username
                if email:
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
                user.save()
            except Exception as e:
                context['updateInvalid'] = True
            finally:
                return render(request, 'settings.html', context)
    else:
        user = User.objects.get(username=request.user.username)
        form = ProfileForm()
        form.set_initial_fields(user)
        context['form'] = form
        return render(request, 'settings.html', context)
    
class AccountForm(forms.Form):
    oldpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput())
    newpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput())
    confirmpassword = forms.CharField(max_length=16, min_length=6, widget=forms.PasswordInput())
 
def account(request):
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
            return render(request, 'account.html', context)
    else:
        context['form'] = AccountForm()
        return render(request, 'account.html', context)

def repositories(request):
    context = {}
    context['title'] = '个人模型概览 | MachLab'
    repos = [{'name':'machlab','size':22},]
    context['repos'] = repos
    return render(request, 'repositories.html', context)

def applications(request):
    context = {}
    context['title'] = '个人应用列表 | MachLab'
    apps = [{'name':'machlab', 'size':22},]
    context['apps'] = apps
    return render(request, 'applications.html', context)