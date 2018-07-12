# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import FileResponse
from urllib import parse
from MachLab.models import ClientPackage

def index(request):
    context          = {}
    context['title'] = '首页 | MachLab'
    return render(request, 'index.html', context)

def download(request):
    context          = {}
    context['title'] = '下载 | MachLab'
    package = ClientPackage.objects.all().first()
    response = FileResponse(package.file)  
    response['Content-Type'] = 'application/x-zip-compressed'  
    response['Content-Disposition'] = 'attachment;filename=' + parse.quote('MachLabClient.zip')
    return response
