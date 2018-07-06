from django.shortcuts import render

def models(request):
    context = {}
    context['title'] = '模型仓库 | MachLab'
    return render(request, 'models.html', context)