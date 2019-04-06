from django import forms
from .models import Topic


class UploadImageForm(forms.ModelForm):
    class Meta:
        model = Topic
        fields = ['image']