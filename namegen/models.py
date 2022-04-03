from django.db import models
from django.conf import settings
from django.utils import timezone

class ActualCharField(models.CharField):
    def db_type(self, connection):
        varchar: str = super().db_type(connection)
        char: str = varchar.replace('varchar', 'char')
        return char

class Country(models.Model):
    name = models.CharField(max_length=75)
    a2_code = ActualCharField(max_length=2)
    a3_code = ActualCharField(max_length=3)
    un_code = ActualCharField(max_length=3)
    has_names = models.BooleanField()
    
    def __str__(self) -> str:
        return self.name

class NamesDB(models.Model):
    country = models.ForeignKey(Country, on_delete=models.DO_NOTHING)
    gender = models.PositiveSmallIntegerField()
    given_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.given_name + self.last_name