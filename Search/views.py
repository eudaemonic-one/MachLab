from django.shortcuts import render
from django.db.models import Q
from MachLab.models import User, Userinfo, Model, Modelfile, ModelCommit, ModelPush, Comment, Star
from MachLab.public import model_type_choices
from Search.search import *

def search(request):    
    context = {}
    q = request.GET.get('q')
    type = request.GET.get('type')
    context['q'] = q
    context['type'] = type
    context['title'] = '搜索'+q+' | MachLab'
    context['username'] = request.user.username

    if q in {'', ' ', '\r', '\n', '\r\n'}:
        context['models'] = None
        context['modelfiles'] = None
        context['commits'] = None
        context['users'] = None
        return render(request, 'search.html', context)
    #elif type == '' or type == 'Models':
    models, result_model_count = search_models(q)
    context['models'] = models
    context['result_model_count'] = result_model_count
    #elif type == 'Modelfiles':
    modelfiles, result_modelfile_count = search_modelfiles(q)
    context['modelfiles'] = modelfiles
    context['result_modelfile_count'] = result_modelfile_count
    #elif type == 'Commits':
    commits, result_commit_count = search_commits(q)
    context['commits'] = commits
    context['result_commit_count'] = result_commit_count
    #elif type == 'Users':
    users, result_user_count = search_users(q)
    context['users'] = users
    context['result_user_count'] = result_user_count
    
    count_list = [result_model_count, result_modelfile_count, result_commit_count, result_user_count,]
    recommend_search_type = get_recommand_search_type(type, count_list)
    context['recommend'] = recommend_search_type

    return render(request, 'search.html', context)
