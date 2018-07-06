# -*- coding: utf-8 -*-
from django import forms
from django.shortcuts import render, reverse, redirect, HttpResponseRedirect
from django.contrib import auth
#from django.contrib.auth.models import User
from MachLab.models import MyUser, MyUserManager
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt 
from django.http import HttpResponse
from django.shortcuts import render

class ProfileForm(forms.Form):
    username = forms.CharField(max_length=16)
    email = forms.EmailField(max_length=32)
    bio = forms.CharField(max_length=256)
    url = forms.CharField(max_length=128)
    location = forms.CharField(max_length=32)
    avatar = forms.ImageField()

    def set_default_values(self,p_username='', p_email='', p_bio='', p_url='', p_location='', p_avatar=''):
        username = forms.CharField(max_length=16, empty_value=p_username)
        email = forms.EmailField(max_length=32, empty_value=p_email)
        bio = forms.CharField(max_length=256, empty_value=p_bio)
        url = forms.CharField(max_length=128, empty_value=p_url)
        location = forms.CharField(max_length=32, empty_value=p_location)
        avatar = forms.ImageField()

@login_required
def profile(request):
    context = {}
    context['title'] = '个人信息概览 | MachLab'
    redirect_to = request.POST.get('next', request.GET.get('next',''))
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
                user = MyUser.objects.get_by_natural_key(request.user.username)
                user.update(username=username, email=email, bio=bio, url=url, location=location, avatar=avatar)
            except Exception as e:
                context['updateInvalid'] = True
            finally:
                return render(request, 'settings.html', context)
    else:
        user = MyUser.objects.get_by_natural_key(request.user.username)
        username = user.get_username()
        email = user.get_email()
        bio = user.get_bio()
        url = user.get_url()
        location = user.get_location()
        avatar = user.get_avatar()
        form = ProfileForm()
        form.set_default_values(username, email, bio, url, location, avatar)
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