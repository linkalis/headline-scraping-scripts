
# coding: utf-8

# In[10]:

import os
import sys
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
import re
from twilio.rest import TwilioRestClient
import settings
import logging
import atexit


# In[11]:

logging.basicConfig(filename='debug.log',level=logging.DEBUG)


# In[12]:

# SOURCES TO SCRAPE: (filename_prefix, url, time_to_scrape, test_css_class)
# use test_css_class to check if the expected content is on the page (otherwise the site may have changed or added an overlay or paywall)

# US & Canada
us1 = ('us_nytimes', 'http://www.nytimes.com', '1200', 'story')
us2 = ('us_nytimes_intl' 'http://international.nytimes.com', '1203', 'story')
us3 = ('us_cnn', 'http://us.cnn.com', '1206', 'cd__headline')
us4 = ('us_cnn_intl', 'http://edition.cnn.com/', '1209', 'cd__headline')
us5 = ('us_usatoday', 'http://www.usatoday.com', '1212', 'js-asset-headline')
us6 = ('us_bostonglobe', 'https://www.bostonglobe.com', '1215', 'story-title')
us7 = ('us_theskimm', 'http://www.theskimm.com/recent', '1218', 'skimm-h1')
us8 = ('us_npr', 'http://www.npr.org', '1221', 'story-text')

ca1 = ('ca_globeandmail', 'http://www.theglobeandmail.com', '1224', 'articleTitle')
ca2 = ('ca_cbc', 'http://www.cbc.ca/news', '1227', 'topstory')
ca3 = ('ca_torontostar', 'https://www.thestar.com', '1230', 'story__headline')
ca4 = ('ca_lapresse', 'http://www.lapresse.ca', '1233', 'moreNews')

us9 = ('us_chicagotribune', 'http://www.chicagotribune.com', '1300', 'trb_outfit_primaryItem_article_title')
us10 = ('us_startribune', 'http://www.startribune.com', '1303', 'tease-headline')
us11 = ('us_cleveland', 'http://www.cleveland.com', '1306', 'fullheadline')

us12 = ('us_latimes', 'http://www.latimes.com', '1500', 'trb_outfit_primaryItem_article_title')
us13 = ('us_nationalenquirer', 'http://www.nationalenquirer.com', '1503', 'postInLine')

# Germany
de1 = ('de_spiegel', 'http://www.spiegel.de', '0600', 'headline')
de2 = ('de_faz', 'http://www.faz.net', '0603', 'Headline')
de3 = ('de_sueddeutsche', 'http://www.sueddeutsche.de', '0606', 'entry-title')
de4 = ('de_bild', 'http://www.bild.de', '0609', 'headline')
de5 = ('de_ard', 'http://www.ard.de', '0612', 'headline')

# Austria?

# France
fr1 = ('fr_lemonde', 'http://www.lemonde.fr', '0615', 'titre_une')
fr2 = ('fr_lefigaro', 'http://www.lefigaro.fr', '0618', 'fig-profil-headline')
fr3 = ('leparisien_url', 'http://www.leparisien.fr', '0621', 'article__title')

# Great Britain
gb1 = ('gb_bbc', 'http://www.bbc.com', '0800', 'media__title')
gb2 = ('gb_guardian', 'http://www.theguardian.com/uk', '0803', 'fc-item__header')
gb3 = ('gb_guardian_intl', 'http://www.theguardian.com/international', '0806', 'fc-item__header')
gb4 = ('gb_dailymail', 'http://www.dailymail.co.uk/home/index.html', '0809', 'article')
gb5 = ('gb_sun', 'https://www.thesun.co.uk', '0812', 'teaser__headline')

#Colombia
co1=('gb_eltiempo', 'http://www.eltiempo.com/' , '2322','caja_articulo')


scraping_list = [us1, us2, us3, us4, us5, us6, us7, us8, us9, us10, us11, us12,
                 ca1, ca2, ca3, ca4,
                 de1, de2, de3, de4, de5,
                 fr1, fr2, fr3, 
                 gb1, gb2, gb3,
                 co1]


# In[13]:

# TWILIO SETTINGS - for SMS error notifications
account_sid = settings.TWILIO_ACCOUNT_SID
auth_token = settings.TWILIO_AUTH_TOKEN
client = TwilioRestClient(account_sid, auth_token)


# In[14]:

# SCRAPE SITE function that's called on a specific site (one at a time) when it's time to scrape a site
def scrape_site(sitename, url, test_css_class):
    filename = sitename + "_" + datetime.utcnow().strftime("%m-%d-%Y_%H%M") + ".html"

    try:
        resp = requests.get(url).text.encode('utf-8')
        soup = BeautifulSoup(resp, 'lxml')
        
        with open(filename, 'w') as outfile:
            outfile.write(soup.prettify())
            logging.info("The web page was saved locally to the file: " + filename)
        
        if soup.find(class_=test_css_class) == None:
            alert = "WARNING! Couldn't find test_css_class on page: " + filename
            logging.warning(alert)
            message = client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body=alert)
        
    except Exception as e:
        alert = "SCRAPING ERROR: " + filename
        if e:
            alert += ". ERROR: " + str(e)
        logging.error(alert)      
        client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body=alert)


# In[15]:

# TO SCRAPE OR NOT TO SCRAPE function that's called every minute to iterate through the scraping list and check if it's time to scrape any of the sites
def to_scrape_or_not_to_scrape(sites_list):
    dt = datetime.utcnow().strftime("%H%M")
    logging.debug("Current time: " + dt)   
    
    for site in sites_list:
        if site[2] == dt:
            logging.debug("Scraping site: " + site[0])
            scrape_site(site[0], site[1], site[3])


# In[16]:

# SCRIPT EXIT function that's sends a text message anytime the script stops running so user can check if it accidentally terminated
def script_exit():
    logging.warning("SCRAPE STOPPED!")
    client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body="SCRAPE STOPPED!")
    
atexit.register(script_exit)


# In[17]:

client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body="SCRAPE STARTING!")


# In[18]:

# WHILE LOOP that executes the main to_scrape_or_not_to_scrape function at 60-second intervals
while True:
    to_scrape_or_not_to_scrape(scraping_list)
    time.sleep(60)


# In[ ]:



