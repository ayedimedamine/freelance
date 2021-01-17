import time
from exceptions.errors import FixErrors

class authentefication :
    def __init__(self,driver):
        self.driver = driver
        self.error_handler = FixErrors()
    
    def login(self,email,password):
        try :
            driver = self.driver
            ea_email = driver.find_element_by_id("email")
            ea_password = driver.find_element_by_id("password")
            login_btn = driver.find_element_by_id('btnLogin')
            ea_email.send_keys(email)
            ea_password.send_keys(password)
            
            login_btn.click()
            time.sleep(0.2)
            try :
                error = driver.find_element_by_class_name('general-error')
                if error.is_displayed():
                    error_handler.ERROR(error.text)
            except Exception :
                print('logged succesfully')
            
            time.sleep(0.5)
            
        except Exception:
            print('cant login')
        finally:
            time.sleep(1)
            driver.quit()