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
chromeOptions.add_argument("--ppapi-flash-path=%s" % ("/tmp/libpepflashplayer.so",))
# /usr/lib/jvm/java-8-oracle/jre/lib/amd64/libnpjp2.so
#chromeOptions.arguments.append('ignore-certificate-errors')
#chromeOptions.add_argument('--ignore-certificate-errors')
#chromeOptions.add_argument("--proxy-server='http=socks5://127.0.0.1:8080'" )
#chromeOptions.arguments.append("proxy-server='%s'"% ("http=127.0.0.1:8080;https=127.0.0.1:8443",))
#chromeOptions.arguments.append("proxy-server='%s'"% ("https=127.0.0.1:8080",))
#chromeOptions.arguments.append("proxy-server='%s'"% ("http=socks5://127.0.0.1:8080;https=socks5://127.0.0.1:8080",))
#chromeOptions.arguments.append("proxy-server='socks5://127.0.0.1:8080'")
chromeOptions.add_argument('--proxy-server=socks5://localhost:8080')
try:
  driver = webdriver.Remote(command_executor='http://127.0.0.1:4444/wd/hub', desired_capabilities = chromeOptions.to_capabilities())
  print "Visiting %s" % (url,)
  #driver.get("https://www.adobe.com/software/flash/about/")
  #time.sleep(5)
  #driver.get("http://javatester.org/version.html")
  #time.sleep(5)
  driver.get("https://www.whatismybrowser.com/")
  def scroll(driver):
    driver.execute_script("""
    function scroll(to) {
      window.scrollTo(0, to);
        to = to + window.innerHeight/64;
          if (to < 10000) {
                  setTimeout(function(){ scroll(to) }, 125);
          }
    }
    to = 0;
    setTimeout(function(){ scroll(to) }, 500);
    """);
  scroll(driver)

  print "Sleeping 3 seconds"
  time.sleep(120)
  #print "Sleeping 60 seconds"
  #time.sleep(60)
  #driver.get("http://sol.no")
  #time.sleep(3)
  #driver.get("http://nrk.no")
  #time.sleep(3)
  print "Closing driver"
  driver.close()
except KeyboardInterrupt:
  print "Closing driver"
  driver.close()
