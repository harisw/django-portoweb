from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='namegen_index'),
    path('file-store/', views.fileStoreIndex, name='namegen_file_store'),
    path('file-store/<slug:slug>/', views.fileStoreGet, name='namegen_file_store_get'),
    path('api/getnames/', views.getNames, name='namegen_getNames'),
]