# -*- coding: utf-8 -*-

from django.shortcuts import render

def index(request):
    context          = {}
    context['title'] = '首页 | MachLab'
    return render(request, 'index.html', context)

def download(request):
    context          = {}
    context['title'] = '下载 | MachLab'
    return render(request, 'download.html', context)
