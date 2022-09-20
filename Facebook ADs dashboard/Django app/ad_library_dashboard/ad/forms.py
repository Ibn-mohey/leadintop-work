from django.forms import ModelForm
from .models import  search_term
class search_terms_form(ModelForm):
    class Meta:
        model = search_term
        fields = ['search_term', 'search_type']