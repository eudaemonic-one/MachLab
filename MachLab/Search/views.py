from django.shortcuts import render
from django.db.models import Q
from MachLab.models import User, Userinfo, Model, Modelfile, ModelCommit, ModelPush, Comment, Star
from MachLab.public import model_type_choices

def search(request):    
    context = {}
    q = request.GET.get('q')
    type = request.GET.get('type')
    if type == '':
        type = 'Models'
    context['q'] = q
    context['type'] = type
    context['title'] = '搜索'+q+' | MachLab'
    context['username'] = request.user.username

    if q == '':
        context['models'] = None
        context['modelfiles'] = None
        context['commits'] = None
        context['users'] = None
        return render(request, 'search.html', context)
#elif type == '' or type == 'Models':
    models = Model.objects.filter(model_name__icontains=q)
    for model in models:
        model.model_type = model_type_choices[model.model_type][1]
    result_model_count = len(models)
    context['models'] = models
    context['result_model_count'] = result_model_count
#elif type == 'Modelfiles':
    modelfiles = Modelfile.objects.filter(filename__icontains=q)
    result_modelfile_count = len(modelfiles)
    context['modelfiles'] = modelfiles
    context['result_modelfile_count'] = result_modelfile_count
#elif type == 'Commits':
    commits = ModelCommit.objects.filter(description__icontains=q)
    result_commit_count = len(commits)
    context['commits'] = commits
    context['result_commit_count'] = result_commit_count
#elif type == 'Users':
    users = User.objects.filter(username__icontains=q)
    result_user_count = len(users)
    context['users'] = users
    context['result_user_count'] = result_user_count
    
    search_type_list = ['Models', 'Modelfiles', 'Commits', 'Users']
    count_list = [result_model_count, result_modelfile_count, result_commit_count, result_user_count,]
    current_search_type = search_type_list.index(type)
    search_type_list.pop(current_search_type)
    count_list.pop(current_search_type)
    recommend_search_type = search_type_list[count_list.index(max(count_list))]
    context['recommend'] = recommend_search_type

    return render(request, 'search.html', context)
