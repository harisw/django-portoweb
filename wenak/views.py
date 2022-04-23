from ast import keyword
import os
import json
from math import ceil
from urllib import request, response
from django.shortcuts import render, get_object_or_404
from .models import Recipe, Category, CategoryType
import csv
from django.conf import settings
import os
from rest_framework import generics
from .serializers import RecipeSerializer
from django.core.paginator import Paginator
from django.http import Http404, JsonResponse, HttpResponse

# Create your views here.
def index(request):
    time_categories = Category.objects(type=CategoryType.TIME.value)
    method_categories = Category.objects(type=CategoryType.COOKING_METHOD.value)
    meat_categories = Category.objects(type=CategoryType.MEAT.value)
    return render(request, 'wenak/wenak.html', {'time_cat': time_categories,
                                                'method_cat': method_categories,
                                                'meat_cat': meat_categories})

def by_category(request, category_type, tag):
    category = get_object_or_404(Category.objects(tag=tag))    
    return render(request, 'wenak/by_category.html', {'category': category})

def by_method(request, method):
    return render(request, 'wenak/by_method.html', {})

def by_meat(request, meat):
    return render(request, 'wenak/by_meat.html', {})

def seed(request):
    csvfile = os.path.join(settings.TEMP_ROOT, 'recipes_with_img.csv')
    file = open(csvfile)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
        ingredients = row[3].replace("'",'').split(',')
        ingredients = [item.lstrip() for item in ingredients]

        steps = row[5].replace("'",'').split(',')
        steps = [i.lstrip() for i in steps]

        tags = row[6].replace("'",'').split(',')
        tags = [i.lstrip() for i in tags]

        ingredient_tags = row[7].replace("'",'').split(',')
        ingredient_tags = [i.lstrip() for i in ingredient_tags]

        rows.append({
            'food_id': row[0],
            'name': row[1],
            'description': row[2],
            'ingredients': ingredients,
            'serving_size': row[4],
            'steps': steps,
            'tags': tags,
            'ingredient_tags': ingredient_tags,
            'views': 0,
            'rating': 0,
            'image': row[8]
        })
    recipe_instances = [Recipe(**data) for data in rows]
    Recipe.objects.insert(recipe_instances, load_bulk=False)
    return render(request, 'wenak/wenak.html', {})

def category_seed(request):
    csvfile = os.path.join(settings.STATIC_ROOT, 'categories_seed.csv')
    file = open(csvfile)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append({
            'name': row[0],
            'type': row[1],
            'description': row[2],
            'image': row[3],
            'tag': row[4],
        })
    category_instances = [Category(**data) for data in rows]
    Category.objects.insert(category_instances, load_bulk=False)
    return render(request, 'wenak/wenak.html', {})

class RecipeListCreate(generics.ListCreateAPIView):
    item_per_page = 10
    queryset = Recipe.objects.limit(item_per_page)
    serializer_class = RecipeSerializer

def recipe_api(request):
    item_per_page = int(request.GET.get('limit', 25))
    page = int(request.GET.get('page', 1))
    tag = request.GET.get('tag', '')
    offset = (page - 1) * item_per_page
    
    if tag != '':
        recipes = Recipe.objects.filter(tags=tag, image__ne='')
    else:
        recipes = Recipe.objects()
    size = recipes.count()
    max_page = ceil(size / item_per_page)
    recipes = recipes.skip(offset).limit(item_per_page)
    dictionaries = [ obj.as_dict() for obj in recipes]
    return HttpResponse(json.dumps({"data": dictionaries, "size": size, "max_page": max_page}), content_type='application/json')

def recipe_detail(request, id):
    recipe = get_object_or_404(Recipe.objects(food_id=id))
    img = recipe.image if recipe.image != None else os.path.join(settings.STATIC_ROOT, "img/placeholder-food.webp")
    return render(request, 'wenak/recipe_detail.html', {'recipe': recipe, 'image': img})

def recipe_search(request):
    keyword = request.GET.get('keyword', '')
    return render(request, 'wenak/recipe_search.html', {'keyword': keyword})

def recipe_api_search(request):
    item_per_page = int(request.GET.get('limit', 25))
    page = int(request.GET.get('page', 1))
    tag = request.GET.get('tag', '')
    keyword = request.GET.get('keyword', '')
    offset = (page - 1) * item_per_page
    
    recipes = Recipe.objects.search_text(keyword)

    if tag != '':
        recipes = recipes.filter(tags=tag)

    size = recipes.count()
    max_page = ceil(size / item_per_page)
    recipes = recipes.skip(offset).limit(item_per_page)
    dictionaries = [ obj.as_dict() for obj in recipes]
    return HttpResponse(json.dumps({"data": dictionaries, "size": size, "max_page": max_page}), content_type='application/json')