def scrape_site(sitename, url, test_css_class, log_errors, send_sms_errors):
    filename = sitename + "_" + datetime.utcnow().strftime("%m-%d-%Y_%H%M") + ".html"

    try:
        resp = requests.get(url).text
        soup = BeautifulSoup(resp, 'lxml')

        with open(filename, 'w') as outfile:
            outfile.write(soup.prettify())
            if log_errors:
                logging.info("The web page was saved locally to the file: " + filename)

        if soup.find(class_=test_css_class) == None:
            alert = "WARNING! Couldn't find test_css_class on page: " + filename
            if log_errors:
                logging.warning(alert)
            if send_sms_errors:
                message = client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body=alert)

    except Exception as e:
        alert = "SCRAPING ERROR: " + filename

        if e:
            alert += ". ERROR: " + str(e)
        if log_errors:
            logging.error(alert)
        if send_sms_errors:
            client.messages.create(to=settings.ALERT_PHONE_NUMBER, from_=settings.TWILIO_PHONE_NUMBER, body=alert)

if __name__ == "__main__":
    import sys
    from datetime import datetime, timedelta
    import requests
    from bs4 import BeautifulSoup
    import logging
    logging.basicConfig(filename = 'debug-scrape_site.log', level = logging.DEBUG)

    sitename = sys.argv[1]
    url = sys.argv[2]
    test_css_class = sys.argv[3]
    log_errors = True
    send_sms_errors = False

    scrape_site(sitename, url, test_css_class, log_errors, send_sms_errors)
