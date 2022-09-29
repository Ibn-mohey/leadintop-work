import re
from django.shortcuts import render,redirect
from django.http import  HttpResponse
from .models import Ads,search_term,facebook_pages
# from django.shortcuts import render_to_response

from .forms import search_terms_form
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
from django.db import IntegrityError


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




####


def home(request):
    if request.method == 'POST':
        req = request.POST
        post_id = req.get('post_id' , '')
        static_id = req.get('static_id' , '')
        
        if post_id != '':
            state = Ads.objects.get(ad_id=post_id).favourite
            Ads.objects.filter(ad_id=post_id).update(favourite = not(state))
        #follow page
        elif static_id != '':
            state = facebook_pages.objects.get(static_ID=static_id).favorites
            facebook_pages.objects.filter(static_ID=static_id).update(favorites = not(state))
            page_name = facebook_pages.objects.get(static_ID=static_id).page_name
            if state  == False:
                try:
                    follow_page = search_term(search_term=page_name, search_type='Page',active=True,static_ID =static_id )
                    follow_page.save()
                except:
                    pass
            elif state == True:
                try:
                    search_term.objects.get(static_ID=static_id).delete()
                except:
                    pass
                

    # if request.method == 'GET':
        
    req = request.GET
    
    sort_by = req.get("sort_by", "-started_date")
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
    if req.get('advertiser','') != '':
        ADS = ADS.filter(page_name__icontains=req['advertiser']).order_by(sort_by)
    if req.get('domain','')  != '':
        ADS = ADS.filter(links__icontains=req['domain']).order_by(sort_by)
    if req.get('action','All') != 'All':
        ADS = ADS.filter(footer_action__icontains=req['action']).order_by(sort_by)
    if req.get('started_date','') != '':

        ADS = ADS.filter(started_date__gte=req['started_date']).order_by('started_date')
    if req.getlist('Advertisers' , []) != []:
        ADS = ADS.filter(reduce(operator.or_, (Q(page_name__icontains=x) for x in req.getlist('Advertisers')))).order_by(sort_by)
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
    P = Paginator(ADS, 21)
    page = request.GET.get('page')
    ADS_list =  P.get_page(page)
    
    nums = "a" * ADS_list.paginator.num_pages
    
    #domains 
    
    domains_side = [link.links for link in ADS]#ADS.values_list('links')
    domains_side = [ urlparse(i).netloc for i in domains_side]
    domains_side = dict(sorted(Counter(domains_side).items(), key=lambda item: item[1],reverse=True))
    domains_side.pop('', 'key not found')
    
    #adv 
    #favs ones 

    advertisers_side = [link.page_name for link in ADS] #ADS.values_list('links') ADS.values_list('page_name')
    advertisers_side = [i for i in advertisers_side]
    advertisers_side = dict(sorted(Counter(advertisers_side).items(), key=lambda item: item[1],reverse=True))
    context = {'valuesss':len(days),
            'pages':ADS_list,
            'ads_data':zip(ADS_list,days),
            'domains':domains_side,
            'advertisers':advertisers_side,
            'Footer_actions':Footer_actions,
            'nums':nums,
            'last_req':dict(request.GET.lists()),
}
    return render(request, 'dashboard/index.html',context)
    # else:
    #     ADS = Ads.objects.all().order_by('-ads_count')
    #     days = [len(set(rec.days.split(','))) for rec in ADS]
    #     P = Paginator(ADS, 20)
    #     page = request.GET.get('page')
    #     ADS_list =  P.get_page(page)
        
    #     nums = "a" * ADS_list.paginator.num_pages
        
    #     #domains 
        
    #     domains_side = [link.links for link in ADS]#ADS.values_list('links')
    #     domains_side = [ urlparse(i).netloc for i in domains_side]
    #     domains_side = dict(sorted(Counter(domains_side).items(), key=lambda item: item[1],reverse=True))
    #     domains_side.pop('', 'key not found')
        
    #     #adv 
    #     #favs ones 

    #     advertisers_side = [link.page_name for link in ADS] #ADS.values_list('links') ADS.values_list('page_name')
    #     advertisers_side = [i for i in advertisers_side]
    #     advertisers_side = dict(sorted(Counter(advertisers_side).items(), key=lambda item: item[1],reverse=True))

    #     context = {'valuesss':len(days),
    #             'pages':ADS_list,
    #             'ads_data':zip(ADS_list,days),
    #             'domains':domains_side,
    #             'advertisers':advertisers_side,
    #             'Footer_actions':Footer_actions,
    #             'nums':nums,}
        
    #     return render(request, 'dashboard/index.html',context)
    # return render(request, 'dashboard/index.html',context)
def get_static_id(link):
    return re.findall(('view_all_page_id=(\d+)'),link)[0]

def add_keyword(request):
    form = search_terms_form()
    terms = search_term.objects.all().order_by('search_term')

    if request.method == 'POST':
        if request.POST.get('action','') == 'ADD':

            try:

                form = search_terms_form(request.POST)
                form.save()

        # code that produces error
            except IntegrityError as e:

                return render(request, "dashboard/search_keys.html", {"message":'value already exist ','form': form,'terms':terms})

            # if form.is_valid():
            #     form.save()
        elif request.POST.get('switch' , '') != '':
            state = search_term.objects.get(id=request.POST.get('switch')).active
            search_term.objects.filter(id=request.POST.get('switch')).update(active = not(state))
        elif request.POST.get('delete' , '') != '':
            current_element =  search_term.objects.get(id=request.POST.get('delete'))
              ### make the id like the switch one 
            if current_element.search_type == 'page':
                 facebook_pages.objects.filter(static_ID=current_element.static_ID).update(favorites = False)
        
            search_term.objects.get(id=request.POST.get('delete')).delete()

    
    return render(request, 'dashboard/search_keys.html', {'form': form,'terms':terms})



def favorites(request):
    if request.method == 'POST':
        req = request.POST
        post_id = req.get('post_id' , '')
        static_id = req.get('static_id' , '')
        if post_id != '':
            state = Ads.objects.get(ad_id=post_id).favourite
            Ads.objects.filter(ad_id=post_id).update(favourite = not(state))
        #follow page
        elif static_id != '':
            state = facebook_pages.objects.get(static_ID=static_id).favorites
            facebook_pages.objects.filter(static_ID=static_id).update(favorites = not(state))
            page_name = facebook_pages.objects.get(static_ID=static_id).page_name
            if state  == False:
                try:
                    follow_page = search_term(search_term=page_name, search_type='Page',active=True,static_ID =static_id )
                    follow_page.save()
                except:
                    pass
            elif state == True:
                try:
                    search_term.objects.get(static_ID=static_id).delete()
                except:
                    pass

    
    # if request.method == 'GET':
    req = request.GET
    pages = facebook_pages.objects.filter(favorites=True).values_list('static_ID')
    pages = [page[0] for page in pages]
    sort_by = req.get("sort_by", "-ads_count")
    ADS = Ads.objects.all().filter( Q(static_id__in=pages) | Q(favourite = True)).order_by('-ads_count')
    
    if sort_by == 'likes_followers':
        sort_by = '-latest_activity_at'
        ADS = Ads.objects.annotate(latest_activity_at=Greatest('page_likes', 'insta_followers')).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    elif sort_by == '-days_running':
        sort_by = "-ads_count"
    else:
        ADS = Ads.objects.all().filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.get('keywords','') != '':
        ADS = ADS.filter(Q(search_term__icontains=req['keywords']) | Q(content__icontains=req['keywords']) ).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.get('advertiser','') != '':
        ADS = ADS.filter(page_name__icontains=req['advertiser']).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.get('domain','')  != '':
        ADS = ADS.filter(links__icontains=req['domain']).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.get('action','All') != 'All':
        ADS = ADS.filter(footer_action__icontains=req['action']).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.get('started_date','') != '':

        ADS = ADS.filter(started_date__gte=req['started_date']).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by('started_date')
    if req.getlist('Advertisers' , []) != []:
        ADS = ADS.filter(reduce(operator.or_, (Q(page_name__icontains=x) for x in req.getlist('Advertisers')))).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
    if req.getlist('domains',[]) != []:
        ADS = ADS.filter(reduce(operator.or_, (Q(links__contains=x) for x in req.getlist('domains')))).filter( Q(static_id__in=pages) | Q(favourite = True)).order_by(sort_by)
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

    P = Paginator(ADS, 21)
    page = request.GET.get('page')
    ADS_list =  P.get_page(page)
    
    nums = "a" * ADS_list.paginator.num_pages
    
    #domains 
    
    domains_side = [link.links for link in ADS]#ADS.values_list('links')
    domains_side = [ urlparse(i).netloc for i in domains_side]
    domains_side = dict(sorted(Counter(domains_side).items(), key=lambda item: item[1],reverse=True))
    domains_side.pop('', 'key not found')
    
    #adv 
    #favs ones 

    advertisers_side = [link.page_name for link in ADS] #ADS.values_list('links') ADS.values_list('page_name')
    advertisers_side = [i for i in advertisers_side]
    advertisers_side = dict(sorted(Counter(advertisers_side).items(), key=lambda item: item[1],reverse=True))
    
    
    
    
    context = {'valuesss':len(days),
               'pages':ADS_list,
               'ads_data':zip(ADS_list,days),
               'domains':domains_side,
               'advertisers':advertisers_side,
               'Footer_actions':Footer_actions,
               'nums':nums,
            'last_req':dict(request.GET.lists()),
    }
    
    return render(request, 'dashboard/favorites.html',context)


