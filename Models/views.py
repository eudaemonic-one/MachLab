from django import forms
from django.forms import widgets
from django.shortcuts import render, reverse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.core.files.base import ContentFile, File
from django.http import FileResponse, HttpResponse
import os
import zipfile
from urllib import parse
from MachLab.models import Userinfo, Model, Modelfile, ModelResult, ModelCommit, ModelPush, ModelPull, ModelDrop, Comment, Star
from MachLab.settings import BASE_DIR
from MachLab.public import model_type_choices

def get_model_info(context, request, username, model_name):
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

    # Star information #
    star = Star.objects.filter(model=model, user=request.user).first()
    if star is not None:
        context['star_type'] = 'unstar'
    else:
        context['star_type'] = 'star'

    # Modelfiles information #
    modelfiles = Modelfile.objects.filter(model=model)
    context['modelfiles'] = modelfiles

    # Latest Commit Information #
    commits = ModelCommit.objects.filter(user=user, model=model)
    latestCommit = commits.order_by('commit_datetime').last()
    context['latestCommit'] = latestCommit

    # Count #
    commit_count = commits.count()
    context['commit_count'] = commit_count
    upload_count = ModelPush.objects.filter(user=user, model=model).count()
    context['upload_count'] = upload_count
    download_count = ModelPull.objects.filter(user=user, model=model).count()
    context['download_count'] = download_count
    comment_count =  Comment.objects.filter(model=model).count()
    context['comment_count'] = comment_count

def models(request, username, model_name):
    context = {}
    context['title'] = '模型仓库 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'files'
    get_model_info(context, request, username, model_name)
    return render(request, 'files.html', context)

def modelfile(request, username, model_name, modelfile_filename):
    context = {}
    context['title'] = '模型仓库 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['modelfile_filename'] = modelfile_filename
    context['active'] = 'files'
    user = User.objects.get(username=username)
    model = Model.objects.filter(user=user, model_name=model_name).first()
    context['model'] = model
    modelfile = Modelfile.objects.filter(model=model, filename=modelfile_filename).first()
    modelfile.text = modelfile.file.readlines()
    modelfile.lines_count = len(modelfile.text)
    modelfile.size = modelfile.file.size
    context['modelfile'] = modelfile
    get_model_info(context, request, username, model_name)
    return render(request, 'modelfile.html', context)

def get_comment_list(context, model):
    comments = Comment.objects.filter(model=model)
    for comment in comments:
        comment.user.username = comment.user.username
        comment.user.avatar = comment.user.userinfo.avatar
        if comment.target is not None:
            comment.target.username = comment.target.user.username
    context['comments'] = comments

def comments(request, username, model_name):
    context = {}
    context['title'] = '模型评论 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'comments'
    user = User.objects.get(username=username)
    model = Model.objects.filter(user=user, model_name=model_name).first()
    get_model_info(context, request, username, model_name)
    get_comment_list(context, model)
    return render(request, 'comments.html', context)

def insights(request, username, model_name):
    context = {}
    context['title'] = '模型结果 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'insights'
    get_model_info(context, request, username, model_name)
    return render(request, 'insights.html', context)

class ModelSettingsForm(forms.Form):
    model_name = forms.CharField(max_length=32)
    model_type = forms.ChoiceField(choices=model_type_choices)
    description = forms.CharField(max_length=256, required=False)
    
    def set_initial_fields(self, model=None):
        if model:
            self.fields['model_name'].initial = model.model_name
            self.fields['model_type'].initial = model.model_type
            self.fields['description'].initial = model.description

def settings(request, username, model_name):
    context = {}
    context['title'] = '模型设置 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'settings'

    if request.user.username == username:
        if request.method == 'POST':
            redirect_to = request.POST.get('next', request.GET.get('next',''))
            form = ModelSettingsForm(request.POST)
            context['form'] = form
            if form.is_valid():
                cd = form.cleaned_data
                new_model_name = cd['model_name']
                new_model_type = cd['model_type']
                new_description = cd['description']
            
                model = Model.objects.filter(model_name=model_name).first()

                if model is not None:
                    new_model = Model.objects.filter(model_name=new_model_name)
                    if new_model is not None:
                        context['alreadyExisted'] = True
                    else:
                        model.model_name = new_model_name
                        model.model_type = new_model_type
                        model.description = new_description
                        model.save()
                    get_model_info(context, request, username, new_model_name)
                    return render(request, 'settings.html', context)
                else:
                    new_model = Model.objects.create(model_name=new_model_name, model_type=new_model_type, description=new_description)
                    new_model.save()
                    get_model_info(context, request, username, model_name)
                    return render(request, 'settings.html', context)
        else:
            model = Model.objects.filter(model_name=model_name).first()
            form = ModelSettingsForm()
            form.set_initial_fields(model)
            context['form'] = form
            get_model_info(context, request, username, model_name)
            return render(request, 'settings.html', context)
    else:
        return HttpResponseRedirect('/')

def upload_modelfile(request, username, model_name):
    context = {}
    context['title'] = '上传 | MachLab'
    #username = request.POST.get('username')
    #model_name = request.POST.get('model_name')
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    upload_file = request.FILES.get('upload_file')

    model = Model.objects.get(model_name=model_name)
    user = User.objects.get(username=username)
    
    filename = upload_file.name
    data = upload_file.file.readlines()
    data.replace(' ', '&nbsp;')
    file = open(filename, 'wt')
    file.write(data)
    file.close()
    modelfile = Modelfile.objects.create(model=model, filename=filename, file=file, description=filename)
    modelfile.save()

    model_push = ModelPush.objects.create(push_name='upload '+len(upload_files)+' file(s) into '+model_name, model=model, user=user, description='upload modelfile')
    model_push.save()

    return models(request, username, model_name)

def download_model(request, username, model_name):
    context = {}
    context['title'] = '下载 | MachLab'
    #username = request.POST.get('username')
    #model_name = request.POST.get('model_name')
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    
    model = Model.objects.get(model_name=model_name)
    user = User.objects.get(username=request.user.username)
    modelfiles = Modelfile.objects.filter(model=model)

    zip_name = model_name+'.zip'
    zip_file = zipfile.ZipFile(zip_name, 'w')
    for modelfile in modelfiles:
        f = open(modelfile.filename, "wt")
        ff = modelfile.file
        ff.open(mode='rt')
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

def new_model(request, username):
    context = {}
    context['title'] = '创建模型 | MachLab'
    context['username'] = username
    context['active'] = 'files'

    if request.user.username == username:
        if request.method == 'POST':
            redirect_to = request.POST.get('next', request.GET.get('next',''))
            form = ModelSettingsForm(request.POST)
            context['form'] = form
            if form.is_valid():
                cd = form.cleaned_data
                new_model_name = cd['model_name']
                new_model_type = cd['model_type']
                new_description = cd['description']
            
                model = Model.objects.filter(model_name=new_model_name).first()

                if model is not None:
                    context['alreadyExisted'] = True
                    return render(request, 'new.html', context)
                    #return HttpResponseRedirect(reverse('user-profile', args=(request.user.username,)))
                else:
                    user = User.objects.get(username=request.user.username)
                    new_model = Model.objects.create(user=user, model_name=new_model_name, model_type=new_model_type, description=new_description)
                    new_model.save()
                    get_model_info(context, request, request.user.username, new_model_name)
                    return render(request, 'files.html', context)
        else:
            form = ModelSettingsForm()
            context['form'] = form
            return render(request, 'new.html', context)
    else:
        return HttpResponseRedirect('/')

def drop_model(request, username, model_name):
    context = {}
    context['title'] = '删除模型 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    redirect_to = request.POST.get('next', request.GET.get('next',''))
    user = User.objects.get(username=request.user.username)
    model = Model.objects.filter(user=user, model_name=model_name).delete()
    return HttpResponseRedirect(redirect_to)

def new_comment(request, username, model_name):
    context = {}
    context['title'] = '新建评论 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'comments'

    model = Model.objects.get(model_name=model_name)
    user = User.objects.get(username=request.user.username)
    target_id = request.POST.get('new-comment-target-id')
    comments = Comment.objects.filter(model=model)
    target = None
    for comment in comments:
        if comment.id == int(target_id):
            target = comment
            break
    
    content = request.POST.get('comment-body')
    comment = Comment.objects.create(model=model, user=user, target=target, content=content)
    comment.save()

    get_model_info(context, request, username, model_name)
    get_comment_list(context, model)
    return render(request, 'comments.html', context)


def delete_comment(request, username, model_name):
    context = {}
    context['title'] = '删除评论 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'comments'

    comment_id = request.POST.get('comment-to-delete-id')
    comment_to_delete = Comment.objects.get(id=int(comment_id))
    comment_to_delete.delete()
    model = Model.objects.get(model_name=model_name)
    
    get_model_info(context, request, username, model_name)
    get_comment_list(context, model)
    return render(request, 'comments.html', context)

def star(request, username, model_name):
    context = {}
    context['title'] = '点赞 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'files'
    redirect_to = request.POST.get('next', request.GET.get('next',''))

    model = Model.objects.filter(model_name=model_name).first()
    user = User.objects.get(username=request.user.username)
    star = Star.objects.create(model=model, user=user)
    star.save()
    model.star_count += 1
    model.save()

    return HttpResponseRedirect(redirect_to)

def unstar(request, username, model_name):
    context = {}
    context['title'] = '取消点赞 | MachLab'
    context['username'] = username
    context['model_name'] = model_name
    context['active'] = 'files'
    redirect_to = request.POST.get('next', request.GET.get('next',''))

    model = Model.objects.filter(model_name=model_name).first()
    user = User.objects.get(username=request.user.username)
    Star.objects.filter(model=model, user=user).delete()
    if model.star_count >= 1:
        model.star_count -= 1
        model.save()

    return HttpResponseRedirect(redirect_to)

def culling(request):
    context = {}
    context['title'] = '模型精选 | MachLab'
    return render(request, 'index.html', context)