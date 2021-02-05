from selenium import webdriver 
from time import sleep
from RedisMaster import Redis_handler
import sys
from config import URL 
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
class Driver: 
    def __init__(self):
        print('setting up ip address')
        #PROXY = FreeProxy().get()
        self.PROXY = 'http://79.137.101.80:45785'
        print('IP ADDR =>', self.PROXY)
        proxy_config = {'httpProxy': self.PROXY, 'sslProxy': self.PROXY}
        proxy_object = Proxy(raw=proxy_config)
        capabilities = DesiredCapabilities.CHROME.copy()
        ua = UserAgent()
        AGENT = ua.random
        capabilities['chrome.switches'] = ['--user-agent=' + AGENT]
        proxy_object.add_to_capabilities(capabilities)
        chrome_options = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images": 2}
        chrome_options.add_experimental_option("prefs", prefs)
        # self.AGENT = ua.random
        print('creating a remote session !')
        self.driverfirefox = webdriver.Remote(
            command_executor='http://161.97.178.112:4444/wd/hub',
            #desired_capabilities={'browserName': 'chrome', 'javascriptEnabled': True}
            desired_capabilities = capabilities,
            options = chrome_options
            )
        # self.driverfirefox = webdriver.Chrome(executable_path=r'C:\Users\MedAmineAydi\Desktop\final\EA_bot\drivers\chromedriver' ,desired_capabilities=capabilities)
        self.redis = Redis_handler()
        print('opening ea url')
        self.driverfirefox.get(URL)
        self.driverfirefox.save_screenshot('done.png')
        executor_url = self.driverfirefox.command_executor._url
        session_id = self.driverfirefox.session_id 
        print('saving session to query ')
        self.redis.init_session(session_id, executor_url)

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
    def end_session(self):
        self.driverfirefox.quit()
        print('session killed !')

    def login(self,my_id, email,password):
        #try :
            #GETTING A FREE SESSION TO LOGIN
            session_firefox = self.redis.get_free_session()
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
            driver = self.attach_to_session(session_firefox['executor_url'], session_firefox['session_id'])
            print("connecting to ur Session .. ")
            #driver.get('https://www.google.com')
            #driver.get('https://www.google.com/search?sxsrf=ALeKk020FnT0zEjfvA2K88ROyo0V62igYw%3A1612385352241&ei=SAwbYPacDsHIlAbSybH4Cg&q=what+is+my+ip&oq=what+is&gs_lcp=CgZwc3ktYWIQAxgAMgQIIxAnMgQIIxAnMgQIIxAnMgQIABBDMgQIABBDMgcIABAUEIcCMgIIADICCAAyAggAMgIIADoCCC46BQgAEJECOgUIABDLAToGCAAQFhAeOgUIABDJAzoFCAAQkgM6BAguEENQ3_kEWJ76BWDIhgZoA3ABeAGAAZ8GiAH9UJIBCjMtMS4xOC4xLjKYAQCgAQGqAQdnd3Mtd2l6wAEB&sclient=psy-ab')
            # driver.save_screenshot('gettingfreesession.png')
            #driver = webdriver.Chrome(options=chrome_options)
            #driver.get(URL)
            #print(driver.current_url)
            print('locating fields ..')
            ea_email = driver.find_element_by_id("email")
            ea_password = driver.find_element_by_id("password")
            login_btn = driver.find_element_by_id('btnLogin')
            print('writing keys')
            ea_email.send_keys(email)
            ea_password.send_keys(password)
            print('all keys sent perfectly ! ',email, password)
            # driver.save_screenshot('before_login_button.png')
            try :
                #driver.set_page_load_timeout(5)
                login_btn.click()
                # driver.save_screenshot('afterClick.png')
                print('login in..')
            except Exception :
                #print(driver.current_url)
                print('cant log in ')
                #btncode = driver.find_element_by_id('btnSendCode')
                #btncode.click()
            try :
                error = driver.find_element_by_class_name('general-error')
                if error.is_displayed():
                    print('error---->',error.text)
                    #driver.get("https://www.google.com/search?q=what+is+my+ip&rlz=1C1SQJL_enTN898TN898&oq=what&aqs=chrome.0.69i59j69i57j69i59j35i39j0i395j69i60j69i61j69i60.1229j1j4&sourceid=chrome&ie=UTF-8")

                    driver.save_screenshot('ifERROR.png')
                    #sys.exit()
                    error_handler.ERROR(error.text)
            except Exception :
                #driver.quit()
                status = 'succ'
                print('logged-in succesfully')
                # driver.save_screenshot('ifSUCC.png')
                #print('here',btncode)
                try:
                    btncode = WebDriverWait(driver, 10).until(
                        EC.presence_of_element_located((By.ID, "btnSendCode"))
                    )
                    btncode.click()
                    print('code sent to email:',email)
                    print('Saving current session')
                    self.redis.save_my_session(my_id,driver.session_id,driver.command_executor._url)
                except Exception:
                    print('cant find the button')
            # btncode.click()
                print(status)
                return status 
            sleep(0.5)

        # except Exception:
        #     #print(driver.current_url)
        #     print('cant login')
    ## wait for it 
    def verify(self, my_id,code):
        print("connecting to ur Session .. ")
        # options = Options()
        session = self.redis.get_my_session(my_id)
        # options.add_argument("--disable-infobars")
        # options.add_argument("--enable-file-cookies")
        #     #options.add_argument('user-agent={}'.format(self.AGENT))
        # capabilities = options.to_capabilities()
        # driver = webdriver.Remote(command_executor=session['executor_url'], desired_capabilities=capabilities)
        # driver.session_id = session['session_id']
        driver = self.attach_to_session(session['executor_url'], session['session_id'])
        driver.save_screenshot('verifySession.png')
        #code = input("your sent code :")
        #driver.save_screenshot("verification0.png")
        print('locating fields ..')
        code_field = driver.find_element_by_id("oneTimeCode")
        print('sending keys')
        code_field.send_keys(code)
        driver.find_element_by_xpath("//a[@id='btnSubmit']/span/span").click()
        print('button clicked')
        

        driver.save_screenshot("final.png")
        cookies = driver.get_cookies()
        cookies = str(cookies).lower()
        cookies = cookies.replace("'",'"')
        print('GOT Cookies')
        driver.quit()
        #################
        # RESET SESSION #
        #################
        self.__init__()
        # executor_url = self.driverfirefox.command_executor._url
        # session_id = self.driverfirefox.session_id
        # driver.delete_all_cookies()
        # driver.get(URL)
        # driver.find_element_by_link_text("Log out and log in as a different user").click()
        # driver.get(URL)
        # #remember-me-panel > li > a.sign-in-different-user
        # self.redis.init_session(session_id,executor_url)
        # self.driverfirefox.save_screenshot('reset_session.png')
        print('session reset')

        #################
        return cookies 
        
        #print(cookies)



# d = Driver()
# print(d)
# # sleep(14)
# d.login('skidrow.crack1@gmail.com','Aminewaka123!')
# d.verify()
# # sleep(10)
# d.end_session()
