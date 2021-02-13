from selenium import webdriver 
from time import sleep
### logger ###
from log.conf_log import logger
### master ###
from RedisMaster import Redis_handler
import sys
from config import URL, PRX, AUTO_PROXY
#####
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.remote.webdriver import WebDriver
# from fp.fp import FreeProxy
from fake_useragent import UserAgent 

def start_new_session(redis):
        ### PROXY ###
        logger.info('THREAD : IP ADDR => {}'.format(AUTO_PROXY))
        proxy_config = {'httpProxy': AUTO_PROXY, 'sslProxy': AUTO_PROXY}
        proxy_object = Proxy(raw=proxy_config)
        capabilities = DesiredCapabilities.CHROME.copy()
        ### USER AGENT ####
        ua = UserAgent()
        AGENT = ua.random
        capabilities['chrome.switches'] = ['--user-agent=' + AGENT]
        proxy_object.add_to_capabilities(capabilities)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        logger.info('THREAD : creating a remote session !')
        d = webdriver.Remote(
            command_executor='http://161.97.178.112:4444/wd/hub',
            desired_capabilities = capabilities,
            options = chrome_options
            )
        logger.info('THREAD : session created succ {{d}}')

        logger.info('THREAD : opening ea url')
        d.get(URL)
        try:
            sleep(3)
            d.save_screenshot('Pushsession.png')
        except:
            logger.warning('THREAD : cant make a screenshot for this new session newsessionTHREAD.png')
        executor_url = d.command_executor._url
        session_id = d.session_id 
        logger.info('THREAD : saving session to query ')
        redis.init_session(session_id, executor_url)
        logger.info('----------> THREAD : DONE RESTORING SESSION')

redis = Redis_handler()
i = 0 
while i < 100 :
    sleep(5)
    start_new_session(redis)
    sleep(5)