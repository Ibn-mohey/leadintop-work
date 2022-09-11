# Create database
import sqlite3
conn = sqlite3.connect('FaceBoookADS2.db')
c = conn.cursor()
try:
    c.execute('''DROP TABLE ads''')
except:
    pass
c.execute('''
CREATE TABLE ads
(AD_ID TEXT PRIMARY KEY, 
Started_date TEXT,
profile_pic TEXT,
links TEXT,
videos TEXT,
content TEXT,
Footer_TEXT TEXT,
Footer_action TEXT,
Page_name TEXT,
AD_occurance INT,
Facebook_ID TEXT,
Page_likes INT,
instgram_ID TEXT,
insta_followers INT,
static_ID TEXT,
Ads_count INT,
cumulative_ads_count INT,
days TEXT,
date TEXT,
hits INT,
search_term TEXT)''')
conn.commit()
conn.close()