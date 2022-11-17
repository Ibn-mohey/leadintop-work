import datetime
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
from django.contrib.auth.decorators import login_required
import json
from django.utils import timezone
from django.contrib.admin.views.decorators import staff_member_required
import requests
import re
from django.http import JsonResponse

# get website data 
sqliteConnection = sqlite3.connect('FaceBoookADS.db')
cursor = sqliteConnection.cursor()
# sqlite_select_query = f"""SELECT links FROM ads where links is not '' """
# cursor.execute(sqlite_select_query)
# domains = cursor.fetchall()

sqlite_select_query = f"""SELECT Page_name FROM ads where Page_name is not '' """
cursor.execute(sqlite_select_query)
advertisers = cursor.fetchall() 

sqlite_select_query = f"""SELECT Footer_action FROM ads where Footer_action is not '' """
cursor.execute(sqlite_select_query)
Footer_actions = cursor.fetchall()

cursor.close()

Footer_actions = [i[0] for i in Footer_actions]
sorted_dict = dict(sorted(Counter(Footer_actions).items(), key=lambda item: item[1],reverse=True))
Footer_actions = dict(sorted_dict.items())
# Footer_actions = dict(itertools.islice(sorted_dict.items(), 5))



with open('countries.json') as f:
    countries = json.load(f)
del countries["EG"]
del countries["SA"]
####

### normal ads
# @login_required(login_url='login')
def home(request):
    if request.method == 'POST':
        req = request.POST
        post_id = req.get('post_id' , '')
        static_id = req.get('static_id' , '')
        # search_page = req.get('search_page','')
        # print("the request", request.get)

        if post_id != '':
            state = Ads.objects.get(ad_id=post_id).favourite
            Ads.objects.filter(ad_id=post_id).update(favourite = not(state))
        #follow page
        elif req.get('block' , ''):
            state = facebook_pages.objects.get(static_ID=req['block']).block
            facebook_pages.objects.filter(static_ID=req['block']).update(block = not(state))
            facebook_pages.objects.filter(static_ID=req['block']).update(block_date = timezone.now())
            if state == False:
                facebook_pages.objects.filter(static_ID=req['block']).update(favorites = False)
            # Ads.objects.filter(static_ID=req['block']).delete()
            pass
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
    
    blocked_pages = facebook_pages.objects.filter(block=True).values_list('static_ID',flat=True)    
    req = request.GET
    print("the request", request.GET)
    ads_in_page = int(req.get("ads_in_page", 50))
    sort_by = req.get("sort_by", "-started_date")
    ADS = Ads.objects.all().order_by('-ads_count')
    if sort_by == 'likes_followers':
        sort_by = '-latest_activity_at'
        ADS = Ads.objects.annotate(latest_activity_at=Greatest('page_likes', 'insta_followers')).order_by(sort_by)
    elif sort_by == '-days_running':
        sort_by = "-ads_count"
    else:
        ADS = Ads.objects.all().order_by(sort_by).exclude(static_id__in=blocked_pages)
    
    
    if req.get('search_page','') != '':
        print(req.get('search_page',''))
        ADS = ADS.filter(static_id = req['search_page']).order_by(sort_by)
    # print(search_page)
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

    P = Paginator(ADS, ads_in_page)
    page = request.GET.get('page')
    ADS_list =  P.get_page(page)
    
    nums = "a" * ADS_list.paginator.num_pages
    
    #domains 
    
    # domains_side = [link.links for link in ADS]#ADS.values_list('links')
    l = [link.links.split("\n") for link in ADS]
    domains_side = [item for sublist in l for item in sublist]
    domains_side = [ urlparse(i).netloc for i in domains_side]
    domains_side = dict(sorted(Counter(domains_side).items(), key=lambda item: item[1],reverse=True))
    domains_side.pop('', 'key not found')
    
    #adv 
    #favs ones 

    advertisers_side = [link.page_name for link in ADS] #ADS.values_list('links') ADS.values_list('page_name')
    advertisers_side = [i for i in advertisers_side]
    advertisers_side = dict(sorted(Counter(advertisers_side).items(), key=lambda item: item[1],reverse=True))
    
    Footer_actions = [link.footer_action for link in ADS]
    Footer_actions = dict(sorted(Counter(Footer_actions).items(), key=lambda item: item[1],reverse=True))
    # Footer_actions = dict(sorted_dict.items())
    request.GET.ads_in_page =  req.get("ads_in_page", 50)
    context = {'valuesss':len(days),
            'pages':ADS_list,
            # 'ads_data':zip(ADS[0:30],days[0:30]),
            'ads_data':zip(ADS_list,days),
            'domains':domains_side,
            'advertisers':advertisers_side,
            'Footer_actions':Footer_actions,
            'nums':nums,
            'countries':countries,
            
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

@login_required(login_url='login')
def add_keyword(request):
    form = search_terms_form()
    terms = search_term.objects.all().order_by('search_term')

    if request.method == 'POST':
        if request.POST.get('action','') == 'ADD':
            if request.POST.get('search_type','') == 'Keyword':
                
                try:
                    form = search_terms_form(request.POST)
                    form.save()

            # code that produces error
                except:
                    return render(request, "dashboard/search_keys.html", {"message":'value already exist ','form': form,'terms':terms})
            elif request.POST.get('search_type','') == 'Advertiser':
                
                print('here')
                try:
                    print(111)
                    link = request.POST['search_term']
                    page = requests.get(link)
                    page_name = re.findall('data:{page:{name:"(.+?)"',page.text)[0]
                    page_name = re.findall('data:{page:{name:"(.+?)"',page.text)[0]
                    static_id = re.findall('view_all_page_id=(\d+)',link)[0]
                    follow_page = search_term(search_term =page_name, search_type='Page',active=True,static_ID =static_id )
                    follow_page.save()
                except Exception as e:
                    print(e)
                    return render(request, "dashboard/search_keys.html", {"message":'invalid link','terms':terms})
                
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

    
    return render(request, 'dashboard/search_keys.html', {'terms':terms,'countries':countries})


@login_required(login_url='login')
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
    
    l = [link.links.split("\n") for link in ADS]
    domains_side = [item for sublist in l for item in sublist]
    domains_side = [ urlparse(i).netloc for i in domains_side]
    domains_side = dict(sorted(Counter(domains_side).items(), key=lambda item: item[1],reverse=True))
    domains_side.pop('', 'key not found')
    
    #adv 
    #favs ones 

    advertisers_side = [link.page_name for link in ADS] #ADS.values_list('links') ADS.values_list('page_name')
    advertisers_side = [i for i in advertisers_side]
    advertisers_side = dict(sorted(Counter(advertisers_side).items(), key=lambda item: item[1],reverse=True))
    
    #CTA
    Footer_actions = [link.footer_action for link in ADS]
    sorted_dict = dict(sorted(Counter(Footer_actions).items(), key=lambda item: item[1],reverse=True))
    Footer_actions = dict(sorted_dict.items())
    Footer_actions.pop('', 'key not found')
    
        
    
    context = {'valuesss':len(days),
               'pages':ADS_list,
               'ads_data':zip(ADS_list,days),
               'domains':domains_side,
               'advertisers':advertisers_side,
               'Footer_actions':Footer_actions,
               'nums':nums,
               'countries':countries,
            'last_req':dict(request.GET.lists()),
    }
    
    return render(request, 'dashboard/favorites.html',context)

#pages 
@login_required(login_url='login')
def pages(request):
    # print(request.POST)
    
    
    #mehtods to follow and block
    # req = 
    ads_in_page = int(request.GET.get("ads_in_page", 50))
    # print(ads_in_page)
    if request.POST.get('follow','') != '':
        state = facebook_pages.objects.get(static_ID=request.POST['follow']).favorites
        facebook_pages.objects.filter(static_ID=request.POST['follow']).update(favorites = not(state))
        page_name = facebook_pages.objects.get(static_ID=request.POST['follow']).page_name
        if state  == False:
            try:
                follow_page = search_term(search_term=page_name, search_type='Page',active=True,static_ID =request.POST['follow'] )
                follow_page.save()
            except:
                pass
        elif state == True:
            try:
                search_term.objects.get(static_ID=request.POST['follow']).delete()
            except:
                pass
    if request.POST.get('block','') != '':
        state = facebook_pages.objects.get(static_ID=request.POST['block']).block
        facebook_pages.objects.filter(static_ID=request.POST['block']).update(block = not(state))
        facebook_pages.objects.filter(static_ID=request.POST['block']).update(block_date = datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")  )#timezone.now().replace(microsecond=0))
        if state == False:
            facebook_pages.objects.filter(static_ID=request.POST['block']).update(favorites = False)
            # Ads.objects.filter(static_ID=req['block']).delete()
    req = request.GET
    # print("the request", request.GET)
    sort_by = req.get("sort_by", "-ads_count")
    pages = facebook_pages.objects.all().filter(block=False).order_by('-ads_count')
    if sort_by == 'likes_followers':
        sort_by = '-latest_activity_at'
        pages = facebook_pages.objects.annotate(latest_activity_at=Greatest('page_likes', 'insta_followers')).order_by(sort_by)
    elif sort_by == '-days_running':
        sort_by = "-ads_count"
    else:
        pages = facebook_pages.objects.all().filter(block=False).order_by(sort_by)
    if req.get('advertiser','') != '':
        print("here")
        pages = pages.filter(page_name__icontains=req['advertiser']).order_by(sort_by)
    
    P = Paginator(pages, ads_in_page)
    page = request.GET.get('page')
    pages_list =  P.get_page(page)
    
    nums = "a" * pages_list.paginator.num_pages
    
    # if not request.GET.ads_in_page:
    request.GET.ads_in_page =  req.get("ads_in_page", 50)
    return render(request, 'dashboard/pages.html',{'pages':pages_list,'valuesss':len(pages),'countries':countries})

@staff_member_required(login_url='login')
def Blocked_Advertiser(request):
    req = request.POST   
    if req.get('block','') != '':
        state = facebook_pages.objects.get(static_ID=req['block']).block
        facebook_pages.objects.filter(static_ID=req['block']).update(block = not(state))
        facebook_pages.objects.filter(static_ID=req['block']).update(block_date = timezone.now())
        if state == False:
            facebook_pages.objects.filter(static_ID=req['block']).update(favorites = False)
    pages = facebook_pages.objects.filter(block=True)
    return render(request, 'dashboard/Blocked_Advertiser.html',{'pages':pages})