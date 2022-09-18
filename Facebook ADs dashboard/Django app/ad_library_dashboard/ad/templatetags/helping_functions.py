from django import template

register = template.Library()
import re
from ..models import Ads

@register.filter(name='get_len_splits')
def get_len_splits(text):
    return len(text.split('\n'))
@register.filter(name='get_all_splits')
def get_all_splits(text):
    return text.split('\n')
@register.filter(name='last_link')
def last_link(text):
    return text.split('\n')[-1]
@register.filter(name='insta_link')
def insta_link(text):
    if text == 'NO insta ID found':
        return ""
    else:
        return text.replace('@', '')
@register.filter('page_ads_link')
def page_ads_link(text):
    return f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&view_all_page_id={text}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=video'
@register.filter('ad_link')
def ad_link(text):
    return f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country=ALL&q={text}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=keyword_unordered&media_type=video'
@register.filter('profile_pic')
def profile_pic(text):
    try:
        name = re.findall('\d+_\d+_\d+_n',text)[0] + '.png'
        return  f'/media/pics/{name}'
    except:
        return ""
@register.filter('video_location')
def video_location(text):
    try:
        name = re.findall('\d+_\d+_\d+_n',text)[0] + '.mp4'
        return f'/media/vids/{name}'
    except:
        return ""



