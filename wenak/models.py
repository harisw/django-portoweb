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
    ingredients = ListField(StringField())
    ingredient_tags = ListField(StringField())
    serving_size = StringField()
    steps = ListField(StringField())
    tags = ListField(StringField())
    views = IntField(min_value=0)
    rating = FloatField(min_value=0)
    def __str__(self) -> str:
        return self.name