from django.urls import path

from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('upload-cv/', views.upload, name="upload-cv"),
    path('download/<path:file_path>/', views.download_file, name='download_file'),
]