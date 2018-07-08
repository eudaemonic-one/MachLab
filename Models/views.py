from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.base import ContentFile, File
from django.http import FileResponse, HttpResponse
import os
import zipfile
from urllib import parse
from MachLab.models import Userinfo, Model, Modelfile, ModelResult, ModelCommit, ModelPush, ModelPull, ModelDrop, Comment
from MachLab.settings import BASE_DIR

def models(request, username, model_name):
    context = {}
    context['title'] = '模型仓库 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    
    # User informtion #
    user = User.objects.get(username=username)
    context['email'] = user.email
    if user.userinfo:
        context['bio'] = user.userinfo.bio
        context['url'] = user.userinfo.url
        context['location'] = user.userinfo.location
        context['avatar'] = user.userinfo.avatar
        
    # Model information #
    model = Model.objects.filter(user=user, model_name=model_name).first()
    context['model'] = model

    # Modelfiles information #
    modelfiles = Modelfile.objects.filter(model=model)
    context['modelfiles'] = modelfiles

    # Latest Commit Information #
    commits = ModelCommit.objects.filter(user=user, model=model)
    latestCommit = commits.order_by('commit_datetime').last()
    context['latestCommit'] = latestCommit

    commit_count = commits.count()
    context['commit_count'] = commit_count
    upload_count = ModelPush.objects.filter(user=user, model=model).count()
    context['upload_count'] = upload_count
    download_count = ModelPull.objects.filter(user=user, model=model).count()
    context['download_count'] = download_count
    comment_count =  Comment.objects.filter(model=model).count()
    context['comment_count'] = comment_count

    return render(request, 'files.html', context)

def issues(request, username, model_name):
    context = {}
    context['title'] = '模型事务 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    return render(request, 'issues.html', context)

def insights(request, username, model_name):
    context = {}
    context['title'] = '模型结果 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    return render(request, 'insights.html', context)

def upload(request):
    context = {}
    context['title'] = '上传 | MachLab'
    username = request.POST.get('username')
    model_name = request.POST.get('model_name')
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    upload_file = request.FILES.get('upload_file')

    model = Model.objects.get(model_name=model_name)
    user = User.objects.get(username=username)
    
    filename = upload_file.name
    file = File(upload_file.file.read())
    modelfile = Modelfile.objects.create(model=model, filename=filename, file=file, description=filename)
    modelfile.save()

    model_push = ModelPush.objects.create(push_name='upload '+len(upload_files)+' file(s) into '+model_name, model=model, user=user, description='upload modelfile')
    model_push.save()

    return models(request, username, model_name)#HttpResponseRedirect(redirect_to)#reverse('models', args=(username,model_name)))

def download(request):
    context = {}
    context['title'] = '下载 | MachLab'
    username = request.POST.get('username')
    model_name = request.POST.get('model_name')
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    
    model = Model.objects.get(model_name=model_name)
    user = User.objects.get(username=request.user.username)
    modelfiles = Modelfile.objects.filter(model=model)

    zip_name = model_name+'.zip'
    zip_file = zipfile.ZipFile(zip_name, 'w')
    for modelfile in modelfiles:
        f = open(modelfile.filename, "wb")
        ff = modelfile.file
        ff.open(mode='rb')
        data = ff.read()
        ff.close()
        f.write(data)
        f.close()
        zip_file.write(modelfile.filename)
    zip_file.close()
    zip_file = open(zip_name, 'rb')
    data = zip_file.read()
    zip_file.close()
    
    for modelfile in modelfiles:
        os.remove(modelfile.filename)

    model_pull = ModelPull.objects.create(model=model, user=user, description='user('+request.user.username+') download model('+model_name+')')
    model_pull.save()

    response = HttpResponse(data, content_type='application/zip')  
    response['Content-Type'] = 'application/octet-stream'  
    response['Content-Disposition'] = 'attachment;filename=' + parse.quote(zip_name)
    return response

def new(request, username, model_name):
    context = {}
    context['title'] = '创建 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    
    return HttpResponseRedirect(reverse('models', args=(username,model_name)))

def drop(request, username, model_name):
    context = {}
    context['title'] = '删除 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    
    return HttpResponseRedirect(reverse('models', args=(username,model_name)))