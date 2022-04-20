from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='wenak_index'),
    path('recipe/<int:id>/', views.recipe_detail, name='recipe_detail'),
    path('recipe/search/', views.recipe_search, name='recipe_search'),
    path('category/<slug:category_type>/<slug:tag>/', views.by_category, name='views_by_category'),
    # path('method/<slug:method>/', views.by_method, name='views_by_method'),
    # path('meat/<slug:meat>/', views.by_meat, name='views_by_meat'),
    path('seed/recipe', views.seed, name='wenak_seed'),
    path('seed/category', views.category_seed),
    path('api/recipe/', views.recipe_api),
    path('api/recipe/search/', views.recipe_api_search)
]