# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.db.models.constraints
from urllib.parse import urlparse
from collections import Counter
import re
class Ads(models.Model):
    ad_id = models.CharField(db_column='AD_ID', primary_key=True,max_length=80)  # Field name made lowercase.
    started_date = models.TextField(db_column='Started_date', blank=True, null=True)  # Field name made lowercase.
    links = models.TextField(blank=True, null=True)
    videos = models.TextField(blank=True, null=True)
    videos_length = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    footer_text = models.TextField(db_column='Footer_TEXT', blank=True, null=True)  # Field name made lowercase.
    footer_action = models.TextField(db_column='Footer_action', blank=True, null=True)  # Field name made lowercase.
    country = models.TextField(blank=True, null=True)
    
    #page
    profile_pic = models.TextField(blank=True, null=True)
    page_name = models.TextField(db_column='Page_name', blank=True, null=True)  # Field name made lowercase.
    facebook_id = models.TextField(db_column='Facebook_ID', blank=True, null=True)  # Field name made lowercase.
    page_likes = models.IntegerField(db_column='Page_likes', blank=True, null=True)  # Field name made lowercase.
    instgram_id = models.TextField(db_column='instgram_ID', blank=True, null=True)  # Field name made lowercase.
    insta_followers = models.IntegerField(blank=True, null=True)
    static_id = models.TextField(db_column='static_ID', blank=True, null=True)  # Field name made lowercase.
    ads_count = models.IntegerField(db_column='Ads_count', blank=True, null=True)  # Field name made lowercase.
    
    ad_occurance = models.IntegerField(db_column='AD_occurance', blank=True, null=True)  # Field name made lowercase.
    cumulative_ads_count = models.IntegerField(blank=True, null=True)
    days = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)
    search_term = models.TextField(blank=True, null=True)
    favourite =  models.BooleanField(default=False)
    poster =  models.TextField(blank=True, null=True)
    state = models.TextField(blank=True, null=True) #state of the file downlaod local or not downloaded or online downloaded 
    
    def get_search_terms(self):
        return " - ".join(list(set(self.search_term.split(','))))
    
    def block_status(self):
        status = facebook_pages.objects.get(static_ID=self.static_id).block 
        if status == True:
            return "fa fa-ban ban" , "blocked"
        elif status == False:
            return "fa fa-ban ban" , "block"
        
    def favorites_status(self):
        if self.favourite == True:
            return "fa fa-star fav faved shadow"
        elif  self.favourite == False:
            return"fa fa-star fav shadow"
    def follow_status(self):
        status = facebook_pages.objects.get(static_ID=self.static_id).favorites 
        if status == True:
            return "fa fa-check-double follow followed" , "followed"
        elif status == False:
            return "fa fa-check-double follow" ,"follow"
    

    class Meta:
        db_table = 'ads'
class search_term(models.Model):
        
    # choices = [('keyword','keyword'),('page','page')]
    countries = [('ALL','ALL'),('EG','EG')]
    search_term =  models.CharField(max_length=80,blank=False, null=False)
    # search_type =  models.TextField(blank=False, null=False,choices = choices)
    search_type =  models.CharField(blank=False, null=False,default='keyword',max_length=80)
    static_ID = models.CharField(blank=True, null=True,max_length=80)
    country = models.CharField(blank=False, null=False,default='ALL',max_length=80)
    active =  models.BooleanField(default=True)
    last_visited = models.TextField(blank=True, null=True)
    # def clean_search_term(self):
    #     if self.search_type == 'advertiser':
            
    #         return re.findall('view_all_page_id=(\d+)',self.search_type)[0]
    #     else:
    #         return self.search_type
    def result_count(self):
        return len(Ads.objects.filter(search_term__icontains=self.search_term))
        pass
    def active_status(self):
        if self.active == True:
            return 'badge badge-success','active'
        elif  self.active == False:
            return 'badge badge-danger','inactive'
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['search_term', 'search_type','country'], name='only_one_search')
        ]
        db_table = 'search_terms'
        
        
class facebook_pages(models.Model):
    static_ID = models.CharField(primary_key=True,max_length=80)
    page_name = models.TextField(blank=False, null=False)
    favorites = models.BooleanField(default=False)
    #new 
    country = models.CharField(blank=True, null=True,max_length=80)
    block = models.BooleanField(default=False)
    profile_pic = models.TextField(blank=True, null=True)
    facebook_id = models.TextField(db_column='Facebook_ID', blank=True, null=True)  # Field name made lowercase.
    page_likes = models.IntegerField(db_column='Page_likes', blank=True, null=True)  # Field name made lowercase.
    instgram_id = models.TextField(db_column='instgram_ID', blank=True, null=True)  # Field name made lowercase.
    insta_followers = models.IntegerField(blank=True, null=True)
    ads_count = models.IntegerField(db_column='Ads_count', blank=True, null=True)  # Field name made lowercase.
    # blocked_date = models.TextField(blank=True, null=True)
    block_date = models.TextField(blank=True, null=True)
    def show_advertise(self):
        return ""
    def find_domain(self):
        l = [link.links.split("\n") for link in Ads.objects.filter(static_id=self.static_ID)]
        flat_list = [item for sublist in l for item in sublist]
        # all_domains  = [ urlparse(i).scheme+"://"+urlparse(i).netloc for i in flat_list]
        all_domains  = [ i for i in flat_list]
        all_domains = dict(sorted(Counter(all_domains).items(), key=lambda item: item[1],reverse=True))
        max_key = max(all_domains, key=all_domains.get, default=0)
        if max_key == '://':
            return "no value"
        return max_key , urlparse(max_key).netloc
    def blocked_status(self):
        if self.block == True:
            return 'disabled' , "Blocked"
        elif self.block == False:
            return '', "Block"
    def follow_status(self):
        if self.block == True:
            return "disabled", 'Blocked'
        if self.favorites == True:
            return "disabled" , 'Followed'
        else:
            return '' , 'Follow'
        
    def favorites_status(self):
        if self.favorites == True:
            return "fa fa-check-double follow followed" , "followed"
        elif  self.favorites == False:
            return "fa fa-check-double follow" ,"follow"
        
    
    class Meta:
        db_table = 'facebook_pages'
