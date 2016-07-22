# Usage Notes

1. Install BeautifulSoup
2. Install lxml: `pip install lxml` (or `pip3 install lxml` on Raspberry Pi)
3. Install Twilio
4. Install datetime

*** Add requirements.txt file instead of individual installs?

4. Create a settings.py file with the following:
`TWILIO_ACCOUNT_SID = "your Twilio account sid here"
TWILIO_AUTH_TOKEN = "your Twilio auth token here"
TWILIO_PHONE_NUMBER = "+15555555555"
ALERT_PHONE_NUMBER = "+15555555555"`


## To use on Raspberry Pi...

### 1) Make sure time is updating on startup

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

The newest versions of Raspbian have both Python 2.7 and Python 3.  This script is written in Python 3, so you will need to run it via `python3 name_of_script.py`, rather than using plain `python`.

### 3) Run the script at startup

Edit crontab -e to have an @reboot event:
`@reboot python3 /home/pi/headline-scraping-scripts/international-news-scraper.py &`

The '&' at the end launches it as a background process so it will keep running but still allow you to launch into the terminal and run other processes on the Pi.
