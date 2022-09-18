from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
import re
from selenium import webdriver
import urllib.request
import urllib.error
from selenium.webdriver.support import expected_conditions as EC
import time
from selenium import webdriver
import time
from selenium import webdriver
from datetime import datetime
import urllib.request
from datetime import datetime
import sqlite3
import requests

driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.facebook.com')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="email"]'))).send_keys('drazahmed1969@gmail.com')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="pass"]'))).send_keys('lordASD4facebook@@' , Keys.ENTER)
def save_log(log):
    print(log)
    with open('log.txt', 'a+') as my_data_file:
        my_data_file.write(f'{log}\n')
        
def open_page(page_id,country= "EG",start_date = None,end_date=None):
    link= f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country}&view_all_page_id={page_id}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&search_type=page&media_type=video'
    driver.get(link)
    time.sleep(2)
def get_ads_number():
    try:
        text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="_7lca"]'))).text
        ADS_count = re.findall('(\d+) result', text)[0]
        tries = 0
        while ADS_count == '0' and tries < 2:
            tries+=1
            driver.refresh()
            time.sleep(5)
            text = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'div[class="_7lca"]'))).text
            ADS_count = re.findall('(\d+) result', text)[0]
            if ADS_count != '0':
                save_log(f"should not be 0,{ADS_count}")
                break
            save_log(f"should be 0, {ADS_count},{tries}")
            time.sleep(300)
    except:
        ADS_count = 0
    return int(ADS_count)
#up date ads count
# sqliteConnection = sqlite3.connect('FaceBoookADS.db')
# cursor = sqliteConnection.cursor()
# sqlite_select_query = f"""SELECT static_ID FROM ads where Ads_count = 0 """
# cursor.execute(sqlite_select_query)
# records = cursor.fetchall()
# page_IDS = [i[0] for i in list(set(records))]
# cursor.close()
# for page_ID in page_IDS:
#     open_page(page_ID)
#     Ads_count = get_ads_number()
#     conn = sqlite3.connect('FaceBoookADS.db')
#     c = conn.cursor()
#     c.execute('''UPDATE ads SET 
#     Ads_count =?,
#     cumulative_ads_count = cumulative_ads_count + ?
#     where static_id = ?'''
#     ,(
#     Ads_count ,
#     Ads_count,
#     page_ID))
#     conn.commit()
#     conn.close()
# driver.close()

#up date id
import sqlite3
sqliteConnection = sqlite3.connect('FaceBoookADS.db')
cursor = sqliteConnection.cursor()
sqlite_select_query = f"""SELECT static_ID, instgram_ID,Facebook_ID FROM ads where instgram_ID = 'NO insta ID found' and Facebook_ID = 'NO Facebook ID found' """
cursor.execute(sqlite_select_query)
records = cursor.fetchall()
page_IDS = [i[0] for i in list(set(records))]
cursor.close()
for page_ID in page_IDS:
    open_page(page_ID)
    Ads_count = get_ads_number()
    conn = sqlite3.connect('FaceBoookADS.db')
    c = conn.cursor()
    c.execute('''UPDATE ads SET 
    Ads_count =?,
    cumulative_ads_count = cumulative_ads_count + ?
    where static_id = ?'''
    ,(
    Ads_count ,
    Ads_count,
    page_ID))
    conn.commit()
    conn.close()
    