from enum import Enum
from bson import ObjectId
from mongoengine import *
from django.conf import settings
from django.utils import timezone
# import environ
# env = environ.Env()
# environ.Env.read_env()

class Recipe(Document):
    name = StringField(max_length=100)
    food_id = IntField()
    description = StringField(null=True)
    image = StringField(max_length=255)
    ingredients = ListField(StringField())
    ingredient_tags = ListField(StringField())
    serving_size = StringField()
    steps = ListField(StringField())
    tags = ListField(StringField())
    views = IntField(min_value=0)
    rating = FloatField(min_value=0)

    def __str__(self) -> str:
        return self.name

    def as_dict(self):
        return {
            'id': self.food_id,
            'name': self.name,
            'description': self.description,
            'rating': self.rating,
            'image': self.image
        }

class CategoryType(Enum):
    TIME = 'time'
    COOKING_METHOD = 'cooking_method'
    MEAT = 'meat'
    def __str__(self) -> str:
        return self.value

class Category(Document):
    name = StringField(max_length=100)
    type = StringField(max_length=50)
    description = StringField(null=True)
    image = StringField(null=True)
    tag = StringField(max_length=75)

    def __str__(self):
        return self.name
    def get_image(self):
        return self.image if self.image != "" else "img/placeholder-food.webp"