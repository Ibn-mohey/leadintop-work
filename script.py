import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium import webdriver
import urllib.request
import socket
import urllib.error
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import random
import threading as th
from selenium import webdriver
from selenium.webdriver.common.proxy import Proxy, ProxyType
import time
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
import requests
import urllib.request
from datetime import datetime
import sqlite3



options = webdriver.ChromeOptions()

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def open_driver():
    return webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def open_link(search_term,country= "EG",start_date = None,end_date=None,media_type='video'):
    link = f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={country}&q={search_term}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={start_date}&start_date[max]={end_date}&search_type=keyword_unordered&media_type=all&media_type={media_type}'
    driver.get(link)
    time.sleep(4)
    
def open_page(page_id,country= "EG",start_date = None,end_date=None):
    link= f'https://www.facebook.com/ads/library/?active_status=all&ad_type=all&country={country}&view_all_page_id={page_id}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=video'
    driver.get(link)
    time.sleep(4)
    
def get_ads_number():
    try:
        text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="gxhhhc31"]'))).text
        ADS_count = re.findall('(\d+) result', text)[0]
        if ADS_count == '0':
            driver.refresh()
            time.sleep(5)
            text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="gxhhhc31"]'))).text
            ADS_count = re.findall('(\d+) result', text)[0]
    except:
        ADS_count = 0
    return ADS_count

def scroll_down(limit = 'no limit'):
    if limit == 'no limit':
        limit = int(get_ads_number())+10
    ads = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')
    temp_ads = 0
    while (len(ads) < limit and temp_ads < len(ads)):
        temp_ads = len(ads)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(3)
        ads = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')
    time.sleep(2)
    
# def find_active(element):
#     return WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,'./div/div[1]/div/div[1]/div[1]/span'))).text


def find_start_date(element):
    return WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,'./div/div[1]/div/div[1]/div[2]/span'))).text[19:]


def find_profile_pic(element):
    try:
        link = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,'.//img[@class="_8nqq img"]'))).get_attribute('src')
        name = re.findall('\d+_\d+_\d+_n',link)[0] + '.png'
        #download
#         img_data = requests.get(link).content
#         with open(name, 'wb') as handler:
#             handler.write(img_data)
        # get path 
        full_path = '' + name
        return full_path
    except:
        return '84702798_579370612644419_4516628711310622720_n.png'


def find_links(element):
    links = "\n".join([a.get_attribute('href') for a in element.find_elements(By.CSS_SELECTOR,'a')[1:] ])
    links = urllib.parse.unquote(links).replace('https://l.facebook.com/l.php?u=', '')
    links = re.findall('(https.+)&',links)
    return "\n".join(links)
# def find_ad_images(element):
#     try:
#         images = WebDriverWait(element,10).until(EC.presence_of_all_elements_located((By.XPATH,'.//img[contains(@class,"_7jys")]')))
#         return "\n".join([a.get_attribute('src') for a in images ])
#     except:
#         return "No images found"
    
def find_ad_videos(element):
    try:
        vids = WebDriverWait(element,10).until(EC.presence_of_all_elements_located((By.XPATH,'.//video')))
        vids_links = [a.get_attribute('src') for a in vids ]
        names = []
        for video in vids_links:
            name = re.findall('\d+_\d+_\d+_n',video)[0] + '.mp4'
#             urllib.request.urlretrieve(video, name)
            names.append(name)
        return "\n".join(names)
    except:
        return "No Videos found"
    
    
def find_content(element):
    return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH,'./div/div[3]/div/div/div[2]/div'))).text


def find_footer(element):
    try:
        footer = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="_8jgz _8jg_"]')))
        action = WebDriverWait(footer, 10).until(EC.presence_of_element_located((By.XPATH,'./div[2]/div/div/span/div/div/div'))).text
        return footer.text , action
    except:
        return "No Footer" , "No Action"


def find_ID(element):
    try:
        return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH, './div/div[1]/div/div[1]/div[4]/div/div/span'))).text[4:]
    except:
        return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH, './div/div[1]/div/div[1]/div[5]/div/div/span'))).text[4:]


# element.find_element(By.XPATH,'./div/div[3]/div/div/div[1]/div/div/div').text.replace("\nSponsored", "")
def find_page_name(element):
    return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH, './div/div[3]/div/div/div[1]/div/div/div'))).text.replace("\nSponsored", "")

def find_ads_occurence(element):
    try:
        return int(element.find_element(By.XPATH, value ='./div/div[1]/div/div[1]/div[5]/span/strong').text.split(' ')[0])
    except:
        return '1'

def click_see_ad_details(element):
    click = WebDriverWait(element, 20).until(EC.element_to_be_clickable((By.XPATH,'./div/div[2]/div/span/div/div/div')))
    driver.execute_script("arguments[0].click();", click)
    time.sleep(0.5)
    return WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="_5aat _4-hy uiLayer _3qw"]')))


