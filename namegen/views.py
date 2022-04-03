from django.shortcuts import render
from .models import Country, NamesDB

# Create your views here.
def index(request):
    countries = Country.objects.filter(has_names=True)
    return render(request, 'home.html', {'countries': countries})