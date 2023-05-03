import os.path
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from business_layer.utilities import *
import zipfile


def unzip_file(filename: str) -> None:
    with zipfile.ZipFile(f'./uploaded/{filename}', 'r') as zip_ref:
        zip_ref.extractall('./uploaded/cvs')


def clear_dirs(directory: str) -> None:
    for filename in os.listdir(directory):
        file_path = os.path.join(directory, filename)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
        except Exception as e:
            print(f'Error deleting {file_path}: {e}')


def extract_info(data: list) -> list:
    list_info: list = list()
    for item in data:
        list_info.append({
            "name": item[0],
            "email": item[1],
            "phone_number": item[2],
            "address": item[3],
            "expert": item[4],
            "expro": item[5],
            "path": item[6].split(','),
            "skills": item[7],
            "score": round(item[-1], 2),
            "image": '_'.join(item[0].split())+".png",
        })
        array_to_img(item[-2], './website/static/website/'+'_'.join(item[0].split())+".png")
    return list_info


def home(request):
    return render(request, 'website/home.html')


def page_not_found_view(request, exception):
    return render(request, 'website/error.html', status=404)


def upload(request):
    clear_dirs('./uploaded')
    clear_dirs('./uploaded/excel')
    clear_dirs('./uploaded/cvs')
    clear_dirs('./website/static/website/')
    if request.method == 'POST' and (request.FILES.get("myFile") or request.FILES.get("myFolder")):
        upload_dir = os.path.join(os.getcwd(), 'uploaded')
        prompt: str = request.POST['prompt'] if request.POST.get("prompt") else ""
        fs = FileSystemStorage(location=upload_dir)
        info = []
        if request.FILES.get("myFolder"):
            folder_zip = request.FILES['myFolder']
            filename_zip = fs.save(folder_zip.name, folder_zip)
            unzip_file(filename_zip)
            data = store_data_xl_dir('./uploaded/cvs', prompt)
            info = extract_info(data)
        else:
            file = request.FILES['myFile']
            filename = fs.save(file.name, file)
            file_name = f'./uploaded/{filename}'
            data = store_data_xl_file(file_name, prompt)
            info = extract_info(data)
        return render(request, 'website/result.html', {"info": info})
    return render(request, 'website/upload-cv.html')


@csrf_exempt
def download_file(request, file_path):
    file_name = os.path.basename(file_path)
    with open(file_path, 'rb') as f:
        response = HttpResponse(f.read())
        response['Content-Type'] = 'application/octet-stream'
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

