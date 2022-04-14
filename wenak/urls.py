from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='wenak_index'),
    path('category/<slug:category>/', views.by_category, name='views_by_category'),
    path('seed/', views.seed, name='wenak_seed'),
    path('api/recipe/', views.RecipeListCreate.as_view())
]