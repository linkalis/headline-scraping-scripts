from selenium import webdriver
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import datetime
import sys

sitename = sys.argv[1]
url = sys.argv[2]

filename = sitename + "_" + datetime.utcnow().strftime("%m-%d-%Y_%H%M") + ".png"

binary = FirefoxBinary("/Macintosh HD/Applications/Firefox")
driver = webdriver.Firefox(firefox_binary=binary)

driver = webdriver.Firefox()
driver.get(url)
driver.save_screenshot(filename)
driver.quit()
