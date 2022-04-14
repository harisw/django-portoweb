from unicodedata import name
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='wenak_index'),
    path('category/<slug:category_type>/<slug:tag>/', views.by_category, name='views_by_category'),
    # path('method/<slug:method>/', views.by_method, name='views_by_method'),
    # path('meat/<slug:meat>/', views.by_meat, name='views_by_meat'),
    path('seed/recipe', views.seed, name='wenak_seed'),
    path('seed/category', views.categorySeed),
    path('api/recipe/', views.RecipeListCreate.as_view())
]