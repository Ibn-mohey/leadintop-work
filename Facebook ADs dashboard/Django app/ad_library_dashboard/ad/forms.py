from django.forms import ModelForm
from .models import  search_term
from django.forms import ModelForm, Textarea,TextInput
class search_terms_form(ModelForm):
    class Meta:
        model = search_term
        fields = ['search_term','country']
        widgets = {
            'search_term': TextInput(attrs={'cols': 80, 'rows': 20}),
        }