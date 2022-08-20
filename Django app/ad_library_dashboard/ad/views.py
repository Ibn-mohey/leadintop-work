from django.shortcuts import render
from django.http import  HttpResponse
from .models import Ads
# Create your views here.


def home(request):
    context = {'range':range(3),
               'ads':Ads.objects.all()[0:5]
        
    }
    return render(request, 'dashboard/index.html',context)