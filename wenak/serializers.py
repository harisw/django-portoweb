from attr import field
#from rest_framework import serializers
from rest_framework_mongoengine import serializers
from .models import Recipe

class RecipeSerializer(serializers.DocumentSerializer):
    class Meta:
        model = Recipe
        fields = ('id','food_id', 'name', 'description', 'ingredients', 'ingredient_tags',
        'serving_size', 'steps', 'tags')