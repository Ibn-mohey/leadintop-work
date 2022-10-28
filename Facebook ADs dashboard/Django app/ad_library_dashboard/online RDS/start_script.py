
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
import cv2
import sys
import argparse
import mysql.connector
from functions import *


parser = argparse.ArgumentParser()

parser.add_argument("--limit", help="enter some quality limit",
                    nargs='?', default='no limit', const=0)
parser.add_argument("--login", help="enter some quality limit",
                    nargs='?', default='yes', const=0)
args = parser.parse_args()




# connect to databsae to get the search terms
# sqliteConnection = sqlite3.connect('FaceBoookADS.db')
# cursor = sqliteConnection.cursor().
mydb = mysql.connector.connect(
  host="database-1.cclpp8z8lgmz.us-east-1.rds.amazonaws.com",
  user="admin",
  password="AWS$2020",
  port = 3306, #for Mamp users
  database='Demo'
)

mycursor = mydb.cursor()

sqlite_select_query = f"""SELECT search_term,country FROM search_terms where active = True and search_type = 'keyword' order by last_visited"""
mycursor.execute(sqlite_select_query)
terms_DB = mycursor.fetchall()
terms = [i[0] for i in terms_DB]
terms_countries =  [i[1] for i in terms_DB]

# terms_countries = [i[1] for i in terms_DB]
sqlite_select_query = f"""SELECT search_term,country FROM search_terms where active = True and search_type = 'page' order by last_visited"""
mycursor.execute(sqlite_select_query)
pages_DB = mycursor.fetchall()
pages = [i[0] for i in pages_DB]
pages_countries = [i[1] for i in pages_DB]
mycursor.close()


# terms = ['perfume']
# terms_countries = ['all']
#start search for the terms 

for term,country in zip(terms,terms_countries):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    #log in 
    if args.login != 'no':
        log_in(driver)  ##reapply
    
    #Log ooooo 
    save_log(f"started the term: {term}")
    #Log ooooo 
    ## start save with limit 'no limit'
    page_IDS = start_save(driver,term,country=country,type= 'keyword',limit=args.limit)
    # sqliteConnection = sqlite3.connect('FaceBoookADS.db')
    # cursor = sqliteConnection.cursor()
    mydb = mysql.connector.connect(
  host="database-1.cclpp8z8lgmz.us-east-1.rds.amazonaws.com",
  user="admin",
  password="AWS$2020",
  port = 3306, #for Mamp users
  database='Demo'
)

    mycursor = mydb.cursor()
    for ID in pages_block_list:
        sqlite_select_query = f"""DELETE FROM ads WHERE static_ID = {ID} """
        mycursor.execute(sqlite_select_query)
    if len(page_IDS)>2:
        sqlite_select_query = f"""update search_terms set last_visited =%s WHERE search_term =%s and search_type = %s and country = %s"""
        mycursor.execute(sqlite_select_query,(datetime.now(),term,'keyword',country))
        mydb.commit()
        mydb.close()
    for page_ID in list(set(page_IDS)):

        open_page(driver,page_ID)
        Ads_count = get_ads_number(driver)
        mydb = mysql.connector.connect(
  host="database-1.cclpp8z8lgmz.us-east-1.rds.amazonaws.com",
  user="admin",
  password="AWS$2020",
  port = 3306, #for Mamp users
  database='Demo'
)
        mycursor = mydb.cursor()
        mycursor.execute('''UPDATE ads SET 
        Ads_count =%s,
        cumulative_ads_count = cumulative_ads_count + %s
        where static_id = %s'''
        ,(
            Ads_count ,
            Ads_count,
            page_ID))
        #insert page into facebook_pages
        mycursor.execute(f"""
        update facebook_pages set 
        Ads_count = %s
        where static_ID = %s
        """,(Ads_count,page_ID))
        mydb.commit()
        mydb.close()
    time.sleep(0.5)
    driver.close()
    
for page,country in zip(pages,pages_countries):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.facebook.com')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="email"]'))).send_keys('drazahmed1969@gmail.com')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="pass"]'))).send_keys('lordASD4facebook@@' , Keys.ENTER)
    time.sleep(0.5)
    #Log ooooo 
    save_log(f"started the page: {page}")
    #Log ooooo 
    page_IDS = start_save(page,country=country,type= 'page')
    sqliteConnection = sqlite3.connect('FaceBoookADS.db')
    cursor = sqliteConnection.cursor()
    for ID in pages_block_list:
        sqlite_select_query = f"""DELETE FROM ads WHERE static_ID = {ID} """
        cursor.execute(sqlite_select_query)
    sqliteConnection.commit()
    sqliteConnection.close()
    time.sleep(0.5)
    driver.close()
    
try:
    driver.close()
    #Log ooooo 
    save_log(f"code finished at : {datetime.now()}")
    exit()
except:
    save_log(f"code finished at : {datetime.now()}")
    exit()
    
#get all with 0 ads 
# sqliteConnection = sqlite3.connect('FaceBoookADS.db')
# cursor = sqliteConnection.cursor()
# sqlite_select_query = f"""SELECT static_ID FROM ads where Ads_count = 0 """
# cursor.execute(sqlite_select_query)
# records = cursor.fetchall()
# page_IDS = [i[0] for i in list(set(records))]
# cursor.close()
# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
# driver.get('https://www.facebook.com')
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

