from .models import PartsImage
from django import forms


class PartsForm(forms.ModelForm):
    class Meta:
        model = PartsImage
        fields = "__all__"
        widgets = {

        }


