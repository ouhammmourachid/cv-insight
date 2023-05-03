import os.path

from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


def home(request):
    return render(request, 'website/home.html')


def result(request):
    return render(request, 'website/result.html',)


def upload(request):
    if request.method == 'POST' and request.FILES["myFile"]:
        file = request.FILES['myFile']
        fs = FileSystemStorage(location=os.path.join(os.getcwd(), 'uploaded'))
        filename = fs.save(file.name, file)
        uploaded_file_url = fs.url(filename)
        print(uploaded_file_url)
        return render(request, 'website/result.html')
    return render(request, 'website/upload-cv.html')


@csrf_exempt
def download_file(request, file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response