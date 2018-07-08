from django.shortcuts import render
from django.contrib.auth.models import User
from MachLab.models import Userinfo, Model

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
        model.model_type = model.choices[model.model_type][1]
    context['models'] = models
    return render(request, 'user-profile.html', context)