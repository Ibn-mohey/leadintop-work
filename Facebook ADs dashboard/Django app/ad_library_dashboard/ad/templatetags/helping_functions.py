from pydoc import doc
from django import template
from ad.models import facebook_pages
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
    
@register.simple_tag(takes_context=True)
def param_replace(context, **kwargs):
    """
    Return encoded URL parameters that are the same as the current
    request's parameters, only with the specified GET parameters added or changed.

    It also removes any empty parameters to keep things neat,
    so you can remove a parm by setting it to ``""``.

    For example, if you're on the page ``/things/?with_frosting=true&page=5``,
    then

    <a href="/things/?{% param_replace page=3 %}">Page 3</a>

    would expand to

    <a href="/things/?with_frosting=true&page=3">Page 3</a>

    Based on
    https://stackoverflow.com/questions/22734695/next-and-before-links-for-a-django-paginated-query/22735278#22735278
    """
    d = context['request'].GET.copy()
    for k, v in kwargs.items():
        d[k] = v
    for k in [k for k, v in d.items() if not v]:
        del d[k]
    return d.urlencode()
