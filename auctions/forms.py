from django import forms
from django.forms import ModelForm
from .models import Listing

from django.core.validators import MinValueValidator


class ListingForm(ModelForm):
    def __init__(self, *args, **kwargs):
        super(ListingForm, self).__init__(*args, **kwargs)
        for field in iter(self.fields):
            self.fields[field].widget.attrs.update({
                'class': 'form-control'
        })
        
    starting_price = forms.DecimalField(required=False, max_digits=6, min_value=1, initial=1)
    class Meta:
        model = Listing
        fields = ['name',
                  'description',
                  'image_url',
                  'category']
