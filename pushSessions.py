from selenium import webdriver 
from time import sleep
### logger ###
from log.conf_log import logger
### master ###
from RedisMaster import Redis_handler
import sys, os
from config import URL, PRX, AUTO_PROXY, HOST
#####
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.remote.webdriver import WebDriver
# from fp.fp import FreeProxy
from fake_useragent import UserAgent 

def start_new_session(redis):
        ### PROXY ###
        print('THREAD : IP ADDR => {}'.format(PRX))
        proxy_config = {'httpProxy': PRX, 'sslProxy': PRX}
        proxy_object = Proxy(raw=proxy_config)
        capabilities = DesiredCapabilities.CHROME.copy()
        ### USER AGENT ####
        ua = UserAgent()
        AGENT = ua.random
        capabilities['chrome.switches'] = ['--user-agent=' + AGENT]
        proxy_object.add_to_capabilities(capabilities)
        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}


        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent='+ AGENT)

        print('THREAD : creating a remote session !')
        d = webdriver.Remote(
            command_executor='http://{}:4444/wd/hub'.format(HOST),
            desired_capabilities = capabilities,
            options = chrome_options
            )
        print('THREAD : session created succ {{d}}')

        print('THREAD : opening ea url')
        d.get(URL)
        # try:
        #     #sleep(3)
        #     d.save_screenshot('Pushsession.png')
        # except:
        #     logger.warning('THREAD : cant make a screenshot for this new session newsessionTHREAD.png')
        executor_url = d.command_executor._url
        session_id = d.session_id 
        print('THREAD : saving session to query ')
        redis.init_session(session_id, executor_url)
        print('----------> THREAD : DONE RESTORING SESSION')

redis = Redis_handler()
i = 0 
import threading
while True:
    if redis.check_available_sessions() == 1 :
        # Restart js render 
        # print('restarting js render ')
        #os.system("docker-compose -f ~/version3/freelance/docker/selenium/docker-compose.yml restart")
        # print('done restarting')
        # Flush redis 
        # redis.flush_sessions()
        sleep(10)
        try :
            start_new_session(redis)
            sleep(5)
        except :
            print('wont work ever :( ')
    elif redis.check_available_sessions() < 12 :
        sleep(1)
        # x= threading.Thread(target=start_new_session,args=redis)
        try:
            start_new_session(redis)
        except :
            # print('restarting js render ')
            # os.system("docker-compose -f ~/version3/freelance/docker/selenium/docker-compose.yml restart")
            # print('done restarting')
            # # Flush redis 
            # redis.flush_sessions()
            # sleep(5)
            # start_new_session(redis)
            print('cant start new session')
    else : 
        #print('nothing to do')
        sleep(1)
# while i < 10 :
#     start_new_session(redis)
#     i+=1
