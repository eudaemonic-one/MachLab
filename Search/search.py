from django.db.models import Q
from MachLab.models import User, Userinfo, Model, Modelfile, ModelCommit, ModelPush, Comment, Star
from MachLab.public import model_type_choices, icon_colors, search_type_list

def search_models(q):
    models = Model.objects.filter(model_name__icontains=q)
    for model in models:
        model.icon_color = icon_colors[model.model_type]
        model.model_type = model_type_choices[model.model_type][1]
    result_model_count = len(models)
    return models, result_model_count

def search_modelfiles(q):
    modelfiles = Modelfile.objects.filter(filename__icontains=q)
    result_modelfile_count = len(modelfiles)
    return modelfiles, result_modelfile_count

def search_commits(q):
    commits = ModelCommit.objects.filter(description__icontains=q)
    result_commit_count = len(commits)
    return commits, result_commit_count

def search_users(q):
    users = User.objects.filter(username__icontains=q)
    result_user_count = len(users)
    return users, result_user_count

def get_recommand_search_type(type, count_list):
    if type == '':
        type = 'Models'
    current_count_list = count_list.copy()
    current_search_type_list = search_type_list.copy()
    current_search_type = search_type_list.index(type)
    current_search_type_list.pop(current_search_type)
    current_count_list.pop(current_search_type)
    recommend_search_type = search_type_list[current_count_list.index(max(current_count_list))]
    return recommend_search_type