# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models
import django.db.models.constraints

class Ads(models.Model):
    ad_id = models.TextField(db_column='AD_ID', primary_key=True, blank=True, null=False)  # Field name made lowercase.
    started_date = models.TextField(db_column='Started_date', blank=True, null=True)  # Field name made lowercase.
    profile_pic = models.TextField(blank=True, null=True)
    links = models.TextField(blank=True, null=True)
    videos = models.TextField(blank=True, null=True)
    content = models.TextField(blank=True, null=True)
    footer_text = models.TextField(db_column='Footer_TEXT', blank=True, null=True)  # Field name made lowercase.
    footer_action = models.TextField(db_column='Footer_action', blank=True, null=True)  # Field name made lowercase.
    page_name = models.TextField(db_column='Page_name', blank=True, null=True)  # Field name made lowercase.
    ad_occurance = models.IntegerField(db_column='AD_occurance', blank=True, null=True)  # Field name made lowercase.
    facebook_id = models.TextField(db_column='Facebook_ID', blank=True, null=True)  # Field name made lowercase.
    page_likes = models.IntegerField(db_column='Page_likes', blank=True, null=True)  # Field name made lowercase.
    instgram_id = models.TextField(db_column='instgram_ID', blank=True, null=True)  # Field name made lowercase.
    insta_followers = models.IntegerField(blank=True, null=True)
    static_id = models.TextField(db_column='static_ID', blank=True, null=True)  # Field name made lowercase.
    ads_count = models.IntegerField(db_column='Ads_count', blank=True, null=True)  # Field name made lowercase.
    cumulative_ads_count = models.IntegerField(blank=True, null=True)
    days = models.TextField(blank=True, null=True)
    date = models.TextField(blank=True, null=True)
    hits = models.IntegerField(blank=True, null=True)
    search_term = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'ads'
class search_term(models.Model):
        
    choices = [('keyword','keyword'),('page','page')]
    search_term =  models.TextField(blank=False, null=False)
    search_type =  models.TextField(blank=False, null=False,choices = choices)
    active =  models.BooleanField(default=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['search_term', 'search_type'], name='only_one_search')
        ]
        db_table = 'search_terms'
