from django.shortcuts import render
from django.http import JsonResponse
from .models import Country, NamesDB

# Create your views here.
def index(request):
    countries = Country.objects.filter(has_names=True)
    return render(request, 'home.html', {'countries': countries})

def getNames(request):
    _country = request.GET.get('country', None)
    _gender = request.GET.get('gender')
    _keyword = request.GET.get('keyword', '')
    
    # if len(_keyword )== 1:
    #     query_keyword = "'"+_keyword+"%'"
    # elif len(_keyword) > 1:
    #     query_keyword = '%'+_keyword
    

    # if len(_keyword) > 0:
    #     namesResult = NamesDB.objects.filter(country_id=_country, gender=_gender,
    #         given_name__icontains=query_keyword)
    # else:
    namesResult = NamesDB.objects.filter(country_id=_country, gender=_gender)

    namesResult = namesResult[:10].values()
    return JsonResponse({'names': list(namesResult)})