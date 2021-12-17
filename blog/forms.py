from django.forms import ModelForm
from rest_framework import fields      
from .models import Photo

class PhotoForm(ModelForm):
  class Meta:
      model = Photo
      fields = ['image']
