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




# driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
def save_log(log):
    print(log)
    with open('log.txt', 'a+') as my_data_file:
        my_data_file.write(f'{log}\n')
#log in facebook
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get('https://www.facebook.com')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="email"]'))).send_keys('drazahmed1969@gmail.com')
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="pass"]'))).send_keys('lordASD4facebook@@' , Keys.ENTER)
time.sleep(0.5)

def open_link(search_term,country= "EG",start_date = None,end_date=None,media_type='video'):
    link = f'https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country={country}&q={search_term}&sort_data[direction]=desc&sort_data[mode]=relevancy_monthly_grouped&start_date[min]={start_date}&start_date[max]={end_date}&search_type=keyword_unordered&media_type=all&media_type={media_type}'
    driver.get(link)
    time.sleep(2)
    
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

def scroll_down(limit = 'no limit'):
    if limit == 'no limit':
         #scroll to end 
        # Get scroll height
        last_height = driver.execute_script("return document.body.scrollHeight")

        while True:
            # Scroll down to bottom
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

            # Wait to load page
            time.sleep(2)

            # Calculate new scroll height and compare with last scroll height
            new_height = driver.execute_script("return document.body.scrollHeight")
            if new_height == last_height:
                break
            last_height = new_height
    
    #scroll enough 
    else:
        ads = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')
        temp_ads = 0
        while (len(ads) < limit and temp_ads < len(ads)):
            temp_ads = len(ads)
            driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(3)
            ads = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')
        time.sleep(2)
        
def find_ID(element):
    try:
        return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH, './div/div[1]/div/div[1]/div[4]/div/div/span'))).text[4:]
    except:
        return WebDriverWait(element,10).until(EC.presence_of_element_located((By.XPATH, './div/div[1]/div/div[1]/div[5]/div/div/span'))).text[4:]


def find_start_date(element):
    text = WebDriverWait(element, 10).until(EC.presence_of_element_located((By.XPATH,'./div/div[1]/div/div[1]/div[2]/span'))).text#[19:]
    date = re.findall('\d+ \S+ \d+',text)[0]
    return datetime.strptime(date,"%d %b %Y" ).strftime("%Y-%m-%d")


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

        return link
    except:
        return  ""  #'84702798_579370612644419_4516628711310622720_n.png'


def find_links(element):
    links = "\n".join([a.get_attribute('href') for a in element.find_elements(By.CSS_SELECTOR,'a')[1:] ])
    links = urllib.parse.unquote(links).replace('https://l.facebook.com/l.php?u=', '')
    links = re.findall('(https.+)&',links)
    return "\n".join(links)

def find_ad_videos(element):
    try:
        vids = WebDriverWait(element,10).until(EC.presence_of_all_elements_located((By.XPATH,'.//video')))
        vids_links = [a.get_attribute('src') for a in vids ]
        names = []
        for video in vids_links:
            name = re.findall('\d+_\d+_\d+_n',video)[0] + '.mp4'
#             urllib.request.urlretrieve(video, name)
            names.append(name)
#         "\n".join(names)
        return "\n".join(vids_links)
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

def get_page_data(element):
    #from the about only 
    
    #MAIN PAGE ELEMENT
    main_element = click_see_ad_details(element)

    #ABOUT THE PAGE ELEMENT
    about_the_page = WebDriverWait(main_element, 10).until(EC.presence_of_element_located((By.XPATH,'./div[2]/div/div/div/div/div[3]/span/div[2]/div/div')))  

    FB_ID = "NO Facebook ID found"
    Insta_ID = "NO insta ID found"
    page_likes = 0
    insta_followers = 0

    try:
        #all pages
        pages = WebDriverWait(about_the_page, 2).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR,'div[class="hael596l alzwoclg c61n2bf6 q46jt4gp bq6c9xl4 r9sb4e79"]')))
        for s in pages:    
            text = s.find_element(By.XPATH,'.').text.replace(',','')
            #facebook 
            if re.search('like', text):
                FB_ID = s.find_element(By.XPATH,'./div[2]/div[1]').text
                page_likes = int(re.findall('(\d+) like' , text)[0])
            if re.search('follower', text):
                Insta_ID = s.find_element(By.XPATH,'./div[2]/div[1]').text
                insta_followers = int(re.findall('(\d+) follower' , text)[0])
    except:
        pass
    
    
    #static ID 
    static_ID = "NO static ID found"
    try:
        page_link = WebDriverWait(main_element, 10).until(EC.presence_of_element_located((By.XPATH,'./div[2]/div/div/div/div/div[3]/span/div[2]/div/div/div[1]/div/a'))).get_attribute('href')
        static_ID = re.findall(('view_all_page_id=(\d+)'),page_link)[0]
        # Open a new window
        driver.execute_script("window.open('');")

        # Switch to the new window and open new URL
        driver.switch_to.window(driver.window_handles[1])
        open_page(static_ID)
        # driver.get(page_link)
        ADS_count = get_ads_number()
        driver.close()

        # Switching to old tab
        driver.switch_to.window(driver.window_handles[0])
    except:
        ADS_count = 0
    time.sleep(0.5)
    webdriver.ActionChains(driver).send_keys(Keys.ESCAPE).perform()
    time.sleep(1) 
#     print(FB_ID, page_likes,Insta_ID,insta_followers, static_ID)
    return FB_ID, page_likes,Insta_ID,insta_followers,static_ID,ADS_count




def start_save(search_term,country= "EG",start_date = None,end_date=None,media_type='video',limit = 'no limit'):
    open_link(search_term,country,start_date,end_date,media_type)
    scroll_down(limit)
    count = 0
    # elements = []
    elements = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')
    while len(elements)==0:
        save_log("no elements")
        time.sleep(300)
        driver.refresh()
        elements = driver.find_elements(By.CSS_SELECTOR, value = 'div[class="_99s5"]')

    for element in elements:
        count =+ 1
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        days = datetime.now().strftime("%d/%m/%Y")
        AD_ID = find_ID(element)
        save_log(AD_ID)
        Started_date = find_start_date(element)
        profile_pic = find_profile_pic(element)
        links = find_links(element)
        videos = find_ad_videos(element)
        content = find_content(element)
        Footer_text , Footer_action = find_footer(element)
        Page_name = find_page_name(element)
        AD_occurance = find_ads_occurence(element)
#         FB_ID, page_likes,Insta_ID,insta_followers, static_ID,ADS_count
        Facebook_ID, Page_likes,instgram_ID , insta_followers, static_ID, Ads_count  = get_page_data(element)
        save_log(time_now)
        # if Ads_count == 0 or Ads_count == "0":
        #     time.sleep(300)
            # driver.refresh()
            # Facebook_ID, Page_likes,instgram_ID , insta_followers, static_ID, Ads_count  = get_page_data(element)
        #save to database   
        try:
        #insert if not exist 
            conn = sqlite3.connect('FaceBoookADS.db')
            c = conn.cursor()
            c.execute('''INSERT INTO ads VALUES 
            (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);'''
                ,(AD_ID ,
                Started_date ,
                profile_pic ,
                links ,
                videos ,
                content ,
                Footer_text ,
                Footer_action ,
                Page_name ,
                AD_occurance ,
                Facebook_ID ,
                Page_likes ,
                instgram_ID ,
                insta_followers ,
                static_ID ,
                Ads_count ,
                Ads_count ,
                days ,
                time_now ,
                1 ,
                search_term ,
                ))
            conn.commit()
            conn.close()
        except:
            #update the data 
            conn = sqlite3.connect('FaceBoookADS.db')
            c = conn.cursor()
            c.execute('''UPDATE ads SET 
            AD_occurance =?,
            Page_likes =?,
            insta_followers =?,
            Ads_count =?,
            cumulative_ads_count = cumulative_ads_count + ?,
            date = ? || ',' || date ,
            days = ?  || ',' || days ,
            hits = hits + 1 , 
            search_term = search_term || ',' || ?   
            where AD_ID = ?'''
              ,(AD_occurance ,
                Page_likes ,
                insta_followers ,
                Ads_count ,
                Ads_count,
                time_now,
                days,
                search_term,
               AD_ID))
            conn.commit()
            conn.close()


terms = '''
عطور
shower 
cream 
scent 
nails
'''.split()

for term in terms:
    save_log(f"started the term: {term}")
    start_save(term)
    time.sleep(0.5)
    driver.close()
    time.sleep(0.5)
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get('https://www.facebook.com')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="email"]'))).send_keys('drazahmed1969@gmail.com')
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR,'input[name="pass"]'))).send_keys('lordASD4facebook@@' , Keys.ENTER)
    time.sleep(0.5)