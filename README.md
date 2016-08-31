# Headline Scraping Scripts

> A webscraper tool using cron on a Raspberry Pi. Also includes optional Twilio text alerts to let you know when your scrapes fail.

## 1) Install requirements

1. Install BeautifulSoup: `pip install beautifulsoup4` (or `pip3 install beautifulsoup4` on Raspberry Pi)
2. Install Twilio python helper library: `pip install twilio` (or `pip3 install twilio` on Raspberry Pi)
3. Install libxml2: `apt-get install libxml2`
4. Install lxml: `apt-get install python3-lxml`
5. Install datetime: `pip install datetime` (or `pip3 install datetime` on Raspberry Pi)

IMPROVEMENT IDEA: Add requirements.txt file instead of individual installs?

## 2) Set up Twilio

If you want to receive text alerts when the scrapes fail, you'll need to set up a Twilio account at Twilio.com.  You can simply sign up for a free trial account, make sure you create a Twilio phone number to send texts from, then find your Twilio SID and auth token.

Next, create a settings.py file and place this file in the top-level project folder so that the scrape_site.py script can import it.  Add the following information to settings.py:

```
TWILIO_ACCOUNT_SID = "your Twilio account sid here"
TWILIO_AUTH_TOKEN = "your Twilio auth token here"
TWILIO_PHONE_NUMBER = "+15555555555"
ALERT_PHONE_NUMBER = "+15555555555"
```

If you **do not** want receive text alerts about the scrapes, simply change the following line in scrape_site.py: `send_sms_errors = True`.  Then, you can comment out all of the lines under "TWILIO SETTINGS" in scrape_site.py.

## 3) Make sure the Raspberry Pi's clock is accurate on startup

If the clock is inaccurate, you may need to force reset it using: `date -s "2016-08-30 20:10:05"`

## 4) Set up your crontab

Scrapes are triggered using cron.  To get started, copy the entire contents of the `crontab` file in this repo into your Pi's crontab by doing the following:

1. Open up the Pi's crontab for editing using crontab -e
2. Select nano (woot woot!) as your editor
3. At the bottom of the crontab, below the comments, do [CTRL] + [R]
4. Enter the full pathname to the crontab file from this repo (for example: /home/pi/headline-scraping-scripts/crontab), then hit [ENTER].  This should copy the entire contents of the file into your actual crontab.

If you want to make sure these cron jobs loaded correctly, you can install a cron graphical editor on Raspberry Pi (`apt-get install gnome-schedule`).  Then, you can check **System Tools** > **Scheduled Tasks**, and you should see all of the scraping jobs listed in there.

If there are other websites you want to scrape, simply add a line for each site to your crontab in the following format.  For example, this will trigger a scrape of example.com every day at 9:30 in the morning:

`30 9 * * * python3 /path/to/scrape_site.py 'sitename' 'http://www.example.com' 'test_css_class'`

## 5) Scrape all the things!

**[FIN]**


## Junk

http://raspberrypi.stackexchange.com/questions/8231/how-to-force-ntpd-to-update-date-time-after-boot

http://askubuntu.com/questions/254826/how-to-force-a-clock-update-using-ntp

https://www.raspberrypi.org/forums/viewtopic.php?f=91&t=16058

chrony
https://www.raspberrypi.org/forums/viewtopic.php?t=69582&p=506585
https://bbs.archlinux.org/viewtopic.php?id=132499

`sudo apt-get install crony`

Set crony password in /etc/crony/crony.keys - replace the randomly-generate password on line 1 with a password of your choice

`sudo nano crontab -e`

add line:
`@reboot chronyc -m "password your-password-from-keys-file" online makestep`



### 2) Run the script as python3

The newest versions of Raspbian for Raspberry Pi have both Python 2.7 and Python 3 pre-installed.  This script is written in Python 3, so you will need to run it via `python3 name_of_script.py`, rather than using plain `python`.

### 3) Run the script at startup

Edit crontab -e to have an @reboot event:
`@reboot python3 /home/pi/headline-scraping-scripts/international-news-scraper.py &`

The '&' at the end launches it as a background process so it will keep running but still allow you to launch into the terminal and run other processes on the Pi.
