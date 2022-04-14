import os
from django.shortcuts import render
from .models import Recipe
import csv
from django.conf import settings
import os
from rest_framework import generics
from .serializers import RecipeSerializer

# Create your views here.
def index(request):
    return render(request, 'wenak/wenak.html', {})

def by_category(request, category):
    return render(request, 'wenak/wenak.html', {})

def seed(request):
    csvfile = os.path.join(settings.STATIC_ROOT, '1k_preprocessedrecipes.csv')
    file = open(csvfile)
    csvreader = csv.reader(file)

    header = []
    header = next(csvreader)
    rows = []
    for row in csvreader:
        rows.append({
            'food_id': row[0],
            'name': row[1],
            'description': row[2],
            'ingredients': row[3].split(','),
            'serving_size': row[4],
            'steps': row[5].split(','),
            'tags': row[6].split(','),
            'ingredient_tags': row[7].split(',')
        })
    recipe_instances = [Recipe(**data) for data in rows]
    Recipe.objects.insert(recipe_instances, load_bulk=False)
    return render(request, 'wenak/wenak.html', {})

class RecipeListCreate(generics.ListCreateAPIView):
    item_per_page = 10
    queryset = Recipe.objects.limit(item_per_page)
    serializer_class = RecipeSerializer