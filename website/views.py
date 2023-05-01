from django.http import HttpResponse
from django.shortcuts import render


def home(request):
    return render(request, 'website/home.html')


def result(request):
    return render(request, 'website/result.html',)


def upload(request):
    return render(request, 'website/upload-cv.html')

