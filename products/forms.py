from django import forms
from .models import Elvis

class ElvisForm(forms.ModelForm):
    class Meta:
        model = Elvis
        fields = ['payment_type', 'name', 'contact', 'promo_code','screenshot']
