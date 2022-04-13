from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponse
from .models import Country, NamesDB, StoredFile
from django.utils import timezone
from django.conf import settings
import pyAesCrypt
import zipfile
import hashlib
import os
import mimetypes

from django.views.generic.edit import FormView
from .forms import UploadFileForm

# Create your views here.
def index(request):
    countries = Country.objects.filter(has_names=True)
    return render(request, 'home.html', {'countries': countries})

def getNames(request):
    _country = request.GET.get('country', None)
    _gender = request.GET.get('gender')
    
    namesResult = NamesDB.objects.filter(country_id=_country, gender=_gender)

    namesResult = namesResult[:10].values()
    return JsonResponse({'names': list(namesResult)})

def fileStoreIndex(request):
    if request.method == "GET":
        return render(request, 'file_storage.html', {})
    elif request.method == "POST":
        customUrl = request.POST.get('customUrl', '')
        password = request.POST.get('password', '')
        now = timezone.now
        expired = request.POST.get('expired')
        
        if customUrl == '':
            customUrl = getCustomUrl()
        
        encrypted_file = handle_uploaded_file(request.FILES, customUrl, password)
        hashed_password = hashlib.md5(password.encode()).hexdigest()
        newStoredFile = StoredFile(slug=customUrl, file_path=encrypted_file, password=hashed_password, expired_at=timezone.now())
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
        
        for file in files.getlist('userfiles'):
            written_path = os.path.join(path, file.name)
            with open(written_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)
            archive.write(written_path, arcname=file.name)
        archive.close()

    if password == '':
        password = name
    
    pyAesCrypt.encryptFile(zip_path, zip_path+".aes", password)
    return name+".zip.aes"

def handle_download_file(file_path, password):
    # Define the full file path
    infile = os.path.join(settings.TEMP_ROOT, file_path)
    outfile = infile[:-3]
    pyAesCrypt.decryptFile(infile, outfile, password)
    # Open the file for reading content
    path = open(outfile, 'rb')
    # Set the mime type
    mime_type, _ = mimetypes.guess_type(outfile)
    # Set the return value of the HttpResponse
    response = HttpResponse(path, content_type=mime_type)
    # Set the HTTP header for sending to browser
    response['Content-Disposition'] = "attachment; filename=%s" % outfile
    # Return the response value
    return response

def fileStoreGet(request, slug):
    file = get_object_or_404(StoredFile, slug=slug)
    if request.method == "GET":
        if file.password == '':
            response = handle_download_file(file.file_path, file.slug)
            return response
        else:
            return render(request, 'file_store_auth.html', {})
    else:
        input_pass = request.POST.get('password', '')
        hashed_inp = hashlib.md5(input_pass.encode()).hexdigest()
        if hashed_inp == file.password:
            response = handle_download_file(file.file_path, input_pass)
            return response
        else:
            return render(request, 'file_store_auth.html', {'error': 'Failed Authentication'})