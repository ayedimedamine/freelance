from selenium import webdriver 
from time import sleep
### logger ###
from log.conf_log import logger
### master ###
from RedisMaster import Redis_handler
import sys,os
from config import URL, PRX, AUTO_PROXY
# from fp.fp import FreeProxy
from fake_useragent import UserAgent
from exceptions.errors import FixErrors
error_handler = FixErrors()
### explicit wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#####
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.common.proxy import Proxy
from selenium.webdriver.remote.webdriver import WebDriver

import threading
class Driver: 
    def __init__(self):
        logger.info('THREAD : setting up ip address')
        #PROXY = FreeProxy().get()
        # sleep(1.5)
        #self.PROXY = 'http://79.137.101.80:45785'
        #self.PROXY = 'http://45.128.187.184:45785'
        #self.PROXY = 'http://45.89.188.55:45785'
        #self.PROXY = "http://91.200.150.55:45785"
        # self.PROXY = "http://212.60.22.63:45785"
        self.PROXY = PRX
        logger.info('THREAD : IP ADDR =>{}'.format(self.PROXY))
        proxy_config = {'httpProxy': self.PROXY, 'sslProxy': self.PROXY}
        proxy_object = Proxy(raw=proxy_config)
        capabilities = DesiredCapabilities.CHROME.copy()
        ua = UserAgent()
        AGENT = ua.random
        capabilities['chrome.switches'] = ['--user-agent=' + AGENT]
        proxy_object.add_to_capabilities(capabilities)
        chrome_options = webdriver.ChromeOptions()
        chrome_prefs = {}
        chrome_options.experimental_options["prefs"] = chrome_prefs
        chrome_prefs["profile.default_content_settings"] = {"images": 2}
        chrome_prefs["profile.managed_default_content_settings"] = {"images": 2}
        logger.info('creating a remote session !')

        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        chrome_options.add_argument('--disable-dev-shm-usage')
        chrome_options.add_argument('--user-agent='+ AGENT)

        self.driverfirefox = webdriver.Remote(
            command_executor='http://144.91.92.58:4444/wd/hub',
            # desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True}
            desired_capabilities = capabilities,
            options = chrome_options
            )
        # self.driverfirefox = webdriver.Chrome(executable_path=r'C:\Users\MedAmineAydi\Desktop\final\EA_bot\drivers\chromedriver' ,desired_capabilities=capabilities)
        self.redis = Redis_handler()
        logger.info('THREAD : opening ea url')
        self.driverfirefox.get(URL)
        # try:
        #     self.driverfirefox.save_screenshot('done.png')
        # except:
        #     logger.warning('THREAD : cant make a screenshot for this new session done.png')
        executor_url = self.driverfirefox.command_executor._url
        session_id = self.driverfirefox.session_id 
        logger.info('THREAD : saving session to query ')
        self.redis.init_session(session_id, executor_url)

    def start_new_session(self):
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
            command_executor='http://144.91.92.58:4444/wd/hub',
            desired_capabilities = capabilities,
            options = chrome_options
            )
        logger.info('THREAD : session created succ',d)

        logger.info('THREAD : opening ea url')
        d.get(URL)
        try:
            d.save_screenshot('newsessionTHREAD.png')
        except:
            logger.warning('THREAD : cant make a screenshot for this new session newsessionTHREAD.png')
        executor_url = d.command_executor._url
        session_id = d.session_id 
        logger.info('THREAD : saving session to query ')
        self.redis.init_session(session_id, executor_url)
        logger.info('----------> THREAD : DONE RESTORING SESSION')

    def attach_to_session(self,executor_url, session_id):
        original_execute = WebDriver.execute
        def new_command_execute(self, command, params=None):
            if command == "newSession":
                # Mock the response
                return {'success': 0, 'value': None, 'sessionId': session_id}
            else:
                return original_execute(self, command, params)
        # Patch the function before creating the driver object
        WebDriver.execute = new_command_execute
        driver = webdriver.Remote(command_executor=executor_url, desired_capabilities={})
        driver.session_id = session_id
        # Replace the patched function with original function
        WebDriver.execute = original_execute
        return driver


    def end_session(self,driver):
        driver.quit()
        logger.warning('session killed !')


    def login(self,my_id, email,password):
        #try :
            #GETTING A FREE SESSION TO LOGIN
            # session_firefox = self.redis.get_free_session()
            # while session_firefox == None :
            #     session_firefox = self.redis.get_free_session()
            #     try :
            #     print('THREAD :SESSION REPLACEMENT ..')
            #     x = threading.Thread(target=self.__init__)
            #     print('THREAD CREATED')
            #     x.start()
            #     print('THREAD : STARTED')
            # except :
            #     print('cant create a new session')
            # try :
            #     print('THREAD :SESSION REPLACEMENT ..')
            #     x = threading.Thread(target=self.__init__)
            #     print('THREAD CREATED')
            #     x.start()
            #     print('THREAD : STARTED')
            # except :
            #     print('cant create a new session')
            # options = Options()
            # options.add_argument("--disable-infobars")
            # options.add_argument("--enable-file-cookies")
            # #options.add_argument('user-agent={}'.format(self.AGENT))
            # capabilities = options.to_capabilities()
            # proxy_config = {'httpProxy': self.PROXY, 'sslProxy': self.PROXY}
            # proxy_object = Proxy(raw=proxy_config)
            # capabilities = DesiredCapabilities.CHROME.copy()
            # proxy_object.add_to_capabilities(capabilities)
            # driver = webdriver.Remote(command_executor=session_firefox['executor_url'], desired_capabilities=capabilities)
            # driver.session_id = session_firefox['session_id']
            # print("connecting to ur Session .. ")
            # driver = self.attach_to_session(session_firefox['executor_url'], session_firefox['session_id'])   
                
            try : 
                if self.redis.check_available_sessions() == 0 :
                    logger.warning("fixing redis issues..")
                    logger.info('restarting js render ..')
                    try:
                        os.system("docker-compose -f ~/final/freelance/docker/selenium/docker-compose.yml restart")
                        logger.info('js render restarted')
                    except :
                        logger.error("cant restart js render ")
                        sleep(6)
                    for i in range(8):
                        try :
                            logger.info('THREAD : SESSION REPLACEMENT ..')
                            x = threading.Thread(target=self.__init__)
                            logger.info('THREAD CREATED')
                            x.start()
                            logger.info('THREAD : STARTED')
                        except :
                            logger.error('THREAD : cant create a new session While true')
                    logger.info("redis works perfectly now !")
                    sleep(2)

            except : 
                logger.error('cant fix empty list in redis')


            while True :
                session_firefox = self.redis.get_free_session()
                logger.info("connecting to a free Session .. ")
                driver = self.attach_to_session(session_firefox['executor_url'], session_firefox['session_id'])
                try:
                    logger.info(driver.current_url)
                    try :
                        logger.info('THREAD : SESSION REPLACEMENT ..')
                        x = threading.Thread(target=self.__init__)
                        logger.info('THREAD CREATED')
                        x.start()
                        logger.info('THREAD : STARTED')
                    except :
                        logger.error('THREAD : cant create a new session While true')
                    
                    logger.info('THREAD : attach to session perfectly')
                    break
                except:
                    logger.warning('trying again')
                    try :
                        logger.info('THREAD : SESSION REPLACEMENT ..')
                        x = threading.Thread(target=self.__init__)
                        logger.info('THREAD CREATED')
                        x.start()
                        logger.info('THREAD : STARTED')
                    except :
                        logger.error('THREAD : cant create a new session While true')

            
            #driver.get('https://www.google.com')
            #driver.get('https://www.google.com/search?sxsrf=ALeKk020FnT0zEjfvA2K88ROyo0V62igYw%3A1612385352241&ei=SAwbYPacDsHIlAbSybH4Cg&q=what+is+my+ip&oq=what+is&gs_lcp=CgZwc3ktYWIQAxgAMgQIIxAnMgQIIxAnMgQIIxAnMgQIABBDMgQIABBDMgcIABAUEIcCMgIIADICCAAyAggAMgIIADoCCC46BQgAEJECOgUIABDLAToGCAAQFhAeOgUIABDJAzoFCAAQkgM6BAguEENQ3_kEWJ76BWDIhgZoA3ABeAGAAZ8GiAH9UJIBCjMtMS4xOC4xLjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab')
            # driver.save_screenshot('gettingfreesession.png')
            #driver = webdriver.Chrome(options=chrome_options)
            #driver.get(URL)
            #print(driver.current_url)
            # try :
            #     driver.save_screenshot('fuck.png')
            # except :
            #     print('cant take screenshot')
            logger.warning('victim : {} {}'.format(email,password))
            logger.info('locating fields ..')
            # ea_email = driver.find_element_by_id("email")
            # ea_password = driver.find_element_by_id("password")
            # login_btn = driver.find_element_by_id('btnLogin')
            # logger.info('writing keys')
            # sleep(1)
            # ea_email.send_keys(email)
            # ea_password.send_keys(password)
            try :
                logger.info('locating email:')
                driver.find_element_by_id("email").send_keys(email)
                logger.info('locating password')
                driver.find_element_by_id("password").send_keys(password)
                
                logger.info('all keys sent perfectly ! ',email, password)
            except:
                return 'unknown error'
            # driver.save_screenshot('before_login_button.png')
            try :
                #driver.set_page_load_timeout(5)
                logger.info('click login')
                driver.find_element_by_xpath("//a[@id='btnLogin']/span/span").click()
                # driver.save_screenshot('afterClick.png')
                logger.info('login in..')
                
            except Exception :
                #print(driver.current_url)
                logger.warning('cant log in ')
                
                ####################
                try :
                    logger.warning('closing session for unvalid login')
                    driver.quit()
                except:
                    logger.error('cant close unvalid login session')

                return 'no_login'
                ####################
                #btncode = driver.find_element_by_id('btnSendCode')
                #btncode.click()
            try :
                error = driver.find_element_by_class_name('general-error')
                if error.is_displayed():
                    logger.error('error----> {} {}'.format(error.text, email))
                    #driver.get("https://www.google.com/search?q=what+is+my+ip&rlz=1C1SQJL_enTN898TN898&oq=what&aqs=chrome.0.69i59j69i57j69i59j35i39j0i395j69i60j69i61j69i60.1229j1j4&sourceid=chrome&ie=UTF-8")
                    error_result = error.text
                    #driver.save_screenshot('ifERROR.png')
                    #sys.exit()
                    
                    ####################
                    try :
                        logger.warning('closing session for unvalid login')
                        driver.quit()
                    except:
                        logger.error('cant close unvalid login session')
                    ####################
                    error_handler.ERROR(error_result)
                    
            except Exception :
                #driver.quit()
                status = 'succ'
                logger.info('logged-in succesfully')
                # driver.save_screenshot('ifSUCC.png')
                #print('here',btncode)
                try:
                    driver.find_element_by_xpath("//a[@id='btnNext']/span/span").click()
                    driver.find_element_by_xpath("//div[@id='panel-tfa-create']/div/div/div/div/div/label").click()
                    driver.find_element_by_xpath("//a[@id='btnTFACreate']/span/span").click()
                    # driver.find_element_by_xpath("//ea-network-nav").click()
                    # driver.find_element_by_xpath("//a[@id='btnSendCode']/span/span").click()
                    logger.info('------- using new method------')
                    # driver.save_screenshot('newnew.png')
                    logger.info('code sent to email:',email)
                    logger.info('Saving current session')
                    self.redis.save_my_session(my_id,driver.session_id,driver.command_executor._url)
                except:
                    #driver.save_screenshot('noluck.png')
                    logger.info('-----using old method----')
                    try:
                        btncode = WebDriverWait(driver, 10).until(
                            EC.presence_of_element_located((By.ID, "btnSendCode"))
                        )
                        btncode.click()
                        logger.info('code sent to email:',email)
                        logger.info('Saving current session')
                        self.redis.save_my_session(my_id,driver.session_id,driver.command_executor._url)
                    except Exception:
                        driver.save_screenshot('damn.png')
                        logger.error('cant find the button')
                        ####################
                        try :
                            logger.warning('closing session for unvalid login')
                            driver.quit()
                        except:
                            logger.error('cant close unvalid login session')
                        ####################
                        return 'fail'
            # btncode.click()
                logger.info(status)
                return status 
            #sleep(0.5)

        # except Exception:
        #     #print(driver.current_url)
        #     print('cant login')
    ## wait for it 
    def verify(self, my_id,code):
        logger.info("connecting to ur Session .. ")
        # options = Options()
        session = self.redis.get_my_session(my_id)
        # options.add_argument("--disable-infobars")
        # options.add_argument("--enable-file-cookies")
        #     #options.add_argument('user-agent={}'.format(self.AGENT))
        # capabilities = options.to_capabilities()
        # driver = webdriver.Remote(command_executor=session['executor_url'], desired_capabilities=capabilities)
        # driver.session_id = session['session_id']
        driver = self.attach_to_session(session['executor_url'], session['session_id'])
        #driver.save_screenshot('verifySession.png')
        #code = input("your sent code :")
        #driver.save_screenshot("verification0.png")
        
        try :  
            logger.info('locating fields ..')
            code_field = driver.find_element_by_id("oneTimeCode")
            logger.info('sending keys')
            code_field.send_keys(code)
            driver.find_element_by_xpath("//a[@id='btnSubmit']/span/span").click()
            logger.info('button clicked')
        except :
            logger.info('NEW : locating fields ..')
            code_field2 = driver.find_element_by_id("twofactorCode")
            logger.info('NEW :sending keys')
            code_field2.send_keys(code)
            driver.find_element_by_xpath("//a[@id='btnTFAVerify']/span").click()
            logger.info('NEW : button clicked')
            
        # driver.save_screenshot("final.png")
        sleep(3)
        # driver.save_screenshot("cookies_final.png")
        cookies = driver.get_cookies()
        cookies = str(cookies).lower()
        cookies = cookies.replace("'",'"')
        logger.info('GOT Cookies')

        #########################
        # print('THREAD :SESSION KILL ..')
        # thead_kill = threading.Thread(target=driver.quit)
        # print('THREAD CREATED')
        # thead_kill.start()
        # print('THREAD : STARTED')
        #########################
        
        driver.quit()

        #################
        # RESET SESSION #
        #################
        # self.__init__()
        # executor_url = self.driverfirefox.command_executor._url
        # session_id = self.driverfirefox.session_id
        # # #remember-me-panel > li > a.sign-in-different-user
        # self.redis.init_session(session_id,executor_url)
        # # self.driverfirefox.save_screenshot('reset_session.png')
        # print('session reset')

        #################
        return cookies 
        
        #print(cookies)

