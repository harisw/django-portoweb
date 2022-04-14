import os
from urllib import response
from django.shortcuts import render
from .models import Recipe
import csv
from django.conf import settings
import os
from rest_framework import generics
from .serializers import RecipeSerializer
from django.core.paginator import Paginator
from django.http import Http404

# Create your views here.
def index(request):
    return render(request, 'wenak/wenak.html', {})

def by_category(request, category):
    categories = ['breakfast', 'lunch', 'dinner', 'desserts']
    if category not in categories:
        raise Http404
    
    page_size = request.GET.get('size', 25);
    page = request.GET.get('page', 1)
    recipes = Recipe.objects(tags=category)
    print(category)
    result = Paginator(recipes, page_size)
    response = result.page(page).object_list
    print(response)
    return render(request, 'wenak/by_category.html', {'page': page, 'recipes': response })

def by_method(request, method):
    return render(request, 'wenak/by_method.html', {})

def by_meat(request, meat):
    return render(request, 'wenak/by_meat.html', {})
def seed(request):
    csvfile = os.path.join(settings.STATIC_ROOT, '1k_preprocessedrecipes.csv')
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
            'rating': 0
        })
    recipe_instances = [Recipe(**data) for data in rows]
    Recipe.objects.insert(recipe_instances, load_bulk=False)
    return render(request, 'wenak/wenak.html', {})

class RecipeListCreate(generics.ListCreateAPIView):
    item_per_page = 10
    queryset = Recipe.objects.limit(item_per_page)
    serializer_class = RecipeSerializer