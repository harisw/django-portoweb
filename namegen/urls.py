from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='namegen_index'),
    path('file-storage/', views.fileStorageIndex, name='namegen_file_storage'),
    path('api/getnames/', views.getNames, name='namegen_getNames'),
]