from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='namegen_index'),
    path('api/getnames/', views.getNames, name='namegen_getNames'),

    path('chatapp', views.chatIndex, name='chat_index')
]