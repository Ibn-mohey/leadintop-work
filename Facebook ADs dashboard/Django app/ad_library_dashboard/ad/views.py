import re
from django.shortcuts import render
from django.http import  HttpResponse
from .models import Ads
from .forms import NameForm
# Create your views here.
from django.http import HttpResponseRedirect
from urllib.parse import urlparse
from collections import Counter
import itertools
import sqlite3
import operator
from django.db.models import Q
from functools import reduce
from urllib.parse import urlparse
from collections import Counter
import itertools
import sqlite3
from itertools import compress
from django.db.models.functions import Greatest
from django.core.paginator import Paginator


# get website data 
sqliteConnection = sqlite3.connect('FaceBoookADS.db')
cursor = sqliteConnection.cursor()
sqlite_select_query = f"""SELECT links FROM ads where links is not '' """
cursor.execute(sqlite_select_query)
domains = cursor.fetchall()

sqlite_select_query = f"""SELECT Page_name FROM ads where Page_name is not '' """
cursor.execute(sqlite_select_query)
advertisers = cursor.fetchall() 

sqlite_select_query = f"""SELECT Footer_action FROM ads where Footer_action is not '' """
cursor.execute(sqlite_select_query)
Footer_actions = cursor.fetchall()

cursor.close()

Footer_actions = [i[0] for i in Footer_actions]
sorted_dict = dict(sorted(Counter(Footer_actions).items(), key=lambda item: item[1],reverse=True))
Footer_actions = dict(itertools.islice(sorted_dict.items(), 5))

advertisers = [i[0] for i in advertisers]
sorted_dict = dict(sorted(Counter(advertisers).items(), key=lambda item: item[1],reverse=True))
advertisers = dict(itertools.islice(sorted_dict.items(), 5))

domains = [ urlparse(i[0]).netloc for i in domains]
sorted_dict = dict(sorted(Counter(domains).items(), key=lambda item: item[1],reverse=True))
domains = dict(itertools.islice(sorted_dict.items(), 5))
####

#post request 
# def home(request):
#     if request.method == 'POST':
#         req = request.POST
        
#         # print()
#         sort_by = req.get("sort_by", "-ads_count")
#         ADS = Ads.objects.all().order_by('-ads_count')
#         if sort_by == 'likes_followers':
#             sort_by = '-latest_activity_at'
#             ADS = Ads.objects.annotate(latest_activity_at=Greatest('page_likes', 'insta_followers')).order_by(sort_by)
#         elif sort_by == '-days_running':
#             sort_by = "-ads_count"
#         else:
#             ADS = Ads.objects.all().order_by(sort_by)
#         if req['keywords'] != '':
#             ADS = ADS.filter(Q(search_term__icontains=req['keywords']) | Q(content__icontains=req['keywords']) ).order_by(sort_by)
#         if req['advertisers'] != '':
#             ADS = ADS.filter(page_name__icontains=req['advertisers']).order_by(sort_by)
#         if req['domain'] != '':
#             ADS = ADS.filter(links__icontains=req['domain']).order_by(sort_by)
#         if req['action'] != 'All':
#             ADS = ADS.filter(footer_action__icontains=req['action']).order_by(sort_by)
#         if req['started_date'] != '':
#             ADS = ADS.filter(started_date__gte=req['started_date']).order_by('started_date')
#         if req.getlist('Advertiser') != []:
#             ADS = ADS.filter(reduce(operator.or_, (Q(page_name__icontains=x) for x in req.getlist('Advertiser')))).order_by(sort_by)
#         if req.getlist('domains') != []:
#             ADS = ADS.filter(reduce(operator.or_, (Q(links__contains=x) for x in req.getlist('domains')))).order_by(sort_by)
#         if req['days'] != '':
#             days = [len(set(rec.days.split(','))) for rec in ADS]
#             cond_list = [True if i > int(req['days']) else False for i in days]
#             ADS  = list(compress(ADS,cond_list))
#         if req.get("sort_by", "-ads_count") == '-days_running':
#             days = []
#             for rec in ADS:
#                 days.append(len(set(rec.days.split(','))))
#             ADS = [x for _, x in sorted(zip(days, ADS), reverse=True, key=lambda pair: pair[0] )]
#         days = [len(set(rec.days.split(','))) for rec in ADS]
#     #not post request        
#     else:
#         ADS = Ads.objects.all().order_by('-ads_count')
#         days = [len(set(rec.days.split(','))) for rec in ADS]
#     P = Paginator(ADS, 20)
#     page = request.GET.get('page')
#     ADS_list =  P.get_page(page)
#     days_list =  P.get_page(page)
#     nums = "a" * ADS_list.paginator.num_pages
    
#     context = {'range':range(3),
#                'pages':ADS_list,
#                'ads_data':zip(ADS_list,days),
#                'file_name' : 'video',
#                'domains':domains,
#                'advertisers':advertisers,
#                'Footer_actions':Footer_actions,
#                'nums':nums,
        
#     }
    
#     return render(request, 'dashboard/index.html',context)


def home(request):
    if request.method == 'GET':
        req = request.GET
        
        # print()
        sort_by = req.get("sort_by", "-ads_count")
        ADS = Ads.objects.all().order_by('-ads_count')
        if sort_by == 'likes_followers':
            sort_by = '-latest_activity_at'
            ADS = Ads.objects.annotate(latest_activity_at=Greatest('page_likes', 'insta_followers')).order_by(sort_by)
        elif sort_by == '-days_running':
            sort_by = "-ads_count"
        else:
            ADS = Ads.objects.all().order_by(sort_by)
        if req.get('keywords','') != '':
            ADS = ADS.filter(Q(search_term__icontains=req['keywords']) | Q(content__icontains=req['keywords']) ).order_by(sort_by)
        if req.get('advertisers','') != '':
            ADS = ADS.filter(page_name__icontains=req['advertisers']).order_by(sort_by)
        if req.get('domain','')  != '':
            ADS = ADS.filter(links__icontains=req['domain']).order_by(sort_by)
        if req.get('action','All') != 'All':
            ADS = ADS.filter(footer_action__icontains=req['action']).order_by(sort_by)
        if req.get('started_date','') != '':
            ADS = ADS.filter(started_date__gte=req['started_date']).order_by('started_date')
        if req.getlist('Advertiser' , []) != []:
            ADS = ADS.filter(reduce(operator.or_, (Q(page_name__icontains=x) for x in req.getlist('Advertiser')))).order_by(sort_by)
        if req.getlist('domains',[]) != []:
            ADS = ADS.filter(reduce(operator.or_, (Q(links__contains=x) for x in req.getlist('domains')))).order_by(sort_by)
        if req.get('days','') != '':
            days = [len(set(rec.days.split(','))) for rec in ADS]
            cond_list = [True if i > int(req['days']) else False for i in days]
            ADS  = list(compress(ADS,cond_list))
        if req.get("sort_by", "-ads_count") == '-days_running':
            days = []
            for rec in ADS:
                days.append(len(set(rec.days.split(','))))
            ADS = [x for _, x in sorted(zip(days, ADS), reverse=True, key=lambda pair: pair[0] )]
        days = [len(set(rec.days.split(','))) for rec in ADS]
    #not post request        
    else:
        ADS = Ads.objects.all().order_by('-ads_count')
        days = [len(set(rec.days.split(','))) for rec in ADS]
    P = Paginator(ADS, 20)
    page = request.GET.get('page')
    ADS_list =  P.get_page(page)
    
    nums = "a" * ADS_list.paginator.num_pages
    
    context = {'range':range(3),
               'pages':ADS_list,
               'ads_data':zip(ADS_list,days),
               'file_name' : 'video',
               'domains':domains,
               'advertisers':advertisers,
               'Footer_actions':Footer_actions,
               'nums':nums,
        
    }
    
    return render(request, 'dashboard/index.html',context)
