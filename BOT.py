######## IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys ## Keyboard KEYS
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities ## dont wait till full loaded
### explicit wait
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
#####
import time
from exceptions.errors import FixErrors
error_handler = FixErrors()
######### PARAMS
#PATH = './drivers/chromedriver.exe'
URL = "https://signin.ea.com/p/web2/login?execution=e1313612656s1&initref=https%3A%2F%2Faccounts.ea.com%3A443%2Fconnect%2Fauth%3Fdisplay%3Dweb2%252Flogin%26scope%3Dbasic.identity%2Boffline%2Bsignin%2Bbasic.entitlement%2Bbasic.persona%26response_type%3Dtoken%26release_type%3Dprod%26redirect_uri%3Dhttps%253A%252F%252Fwww.ea.com%252Ffifa%252Fultimate-team%252Fweb-app%252Fauth.html%26accessToken%3Dnull%26locale%3Den_US%26prompt%3Dlogin%26client_id%3DFIFA21_JS_WEB_APP"
######### CONFIG
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#chromeOptions = Options()
#caps = DesiredCapabilities().CHROME
#caps["pageLoadStrategy"] = "none"
#chromeOptions.headless = True
#driver = webdriver.Chrome(executable_path=PATH,desired_capabilities=caps)#, options=chromeOptions)

######### LOGIN FUNCTION 
def login(email,password,driver):
    try :
        #driver = webdriver.Chrome(options=chrome_options)
        driver.get(URL)
        print(driver.current_url)
        ea_email = driver.find_element_by_id("email")
        ea_password = driver.find_element_by_id("password")
        login_btn = driver.find_element_by_id('btnLogin')

        ea_email.send_keys(email)
        ea_password.send_keys(password)
        print('key send good')
        try :
            #driver.set_page_load_timeout(5)
            login_btn.click()
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
                error_handler.ERROR(error.text)
        except Exception :
            #driver.quit()
            status = 'succ'
            print('logged-in succesfully')
            
            #print('here',btncode)
            try:
                btncode = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.ID, "btnSendCode"))
                )
                btncode.click()
                print(driver.current_url)
            except Exception:
                print('cant find the button')
           # btncode.click()
            print(status)
            return status 
        time.sleep(0.5)

    except Exception:
        #print(driver.current_url)
        print('cant login')
    finally:
        
        print('done')
        #driver.quit()

#login('skidrow.crack1gmail.com','xDTN886x6DipX-$')
