from django import forms

class UploadFileForm(forms.Form):
    file = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))
    password = forms.CharField()
    duration = forms.IntegerField()
    customUrl = forms.CharField()