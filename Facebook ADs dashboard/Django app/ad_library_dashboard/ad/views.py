from django.shortcuts import render
from django.http import  HttpResponse
from .models import Ads
from .forms import NameForm
# Create your views here.

ALL_ADS = Ads.objects.all()
def home(request):
    if request.method == 'POST':
        form = NameForm(request.POST)
    context = {'range':range(3),
               'ads':ALL_ADS[0:6]
        
    }
    return render(request, 'dashboard/index.html',context)