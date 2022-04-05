from django.shortcuts import render
from django.http import JsonResponse
from .models import Country, NamesDB, StoredFile
from django.utils import timezone
from django.conf import settings
import pyAesCrypt
import zipfile
import hashlib
import os

from django.views.generic.edit import FormView
from .forms import UploadFileForm

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

def fileStorageIndex(request):
    if request.method == "GET":
        return render(request, 'file_storage.html', {})
    elif request.method == "POST":
        customUrl = request.POST.get('customUrl', '')
        password = request.POST.get('password', '')
        now = timezone.now
        expired = request.POST.get('expired')
        print(request.POST)
        if customUrl == '':
            customUrl = getCustomUrl()
        
        encrypted_file = handle_uploaded_file(request.FILES, customUrl, password)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        newStoredFile = StoredFile(slug=customUrl, file_path=encrypted_file, password=hashed_password, expired_at=expired)
        newStoredFile.save()
        return render(request, 'file_storage.html', {})

def getCustomUrl():
    newUrl = hashlib.md5(timezone.now.encode()).hexdigest()[:5]
    i = 0
    while len(StoredFile.objects.filter(slug=newUrl).values()) > 0:
        newUrl += i
        i += 1
    return newUrl

def handle_uploaded_file(files, name, password):
    path = settings.TEMP_ROOT
    zip_path = os.path.join(path, name+".zip")
    with zipfile.ZipFile(zip_path, mode="w") as archive:
        for file in files.getlist('file'):
            with open(path / file.name, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            archive.write(file.name)
    pyAesCrypt.encryptFile(zip_path, zip_path+".aes", password)
    return name+".zip.aes"
