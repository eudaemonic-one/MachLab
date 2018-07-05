from django.shortcuts import render

def docs(request, tag=''):
    context = {}
    context['title'] = '文档 | MachLab'
    return render(request, 'docs.html', context)

def overview(request, tag=''):
    context = {}
    context['title'] = '文档概览 | MachLab'
    return render(request, 'overview.html', context)

def setup(request, tag=''):
    context = {}
    context['title'] = '安装手册 | MachLab'
    return render(request, 'setup.html' + tag, context)

def userguide(request, tag=''):
    context = {}
    context['title'] = '用户指南 | MachLab'
    return render(request, 'userguide.html', context)

def faq(request):
    context = {}
    context['title'] = 'FAQ | MachLab'
    return render(request, 'faq.html', context)