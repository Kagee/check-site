#! /usr/bin/env python2
import sys

if len(sys.argv) < 3:
    print "Usage: %s <url> <timestamp>" % (sys.argv[0],)
    sys.exit(1)

url=sys.argv[1]
user_agent=sys.argv[2]
time_start=sys.argv[3]

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
# from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
chromeOptions = webdriver.ChromeOptions(); 
chromeOptions.arguments.append("user-agent='%s'"% (user_agent,))
chromeOptions.arguments.append("ssl-key-log-file=/data/ssl-key-log-%s.log" % (time_start,))
chromeOptions.arguments.append("start-maximized")
chromeOptions.arguments.append("disable-http2")
driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities = chromeOptions.to_capabilities())
driver.get(url)
time.sleep(10)
driver.close()
