class FixErrors :
    def __init__(self):
        super().__init__()
    
    def email_error(self,error):
        if error == "Email address is invalid" :
            return ('Email address is invalid')
    
    def login_error(self,error):
        if error != "Email address is invalid" :
            return ('Your credentials are incorrect or have expired. Please try again or reset your password.')

    def ERROR(self,error):
        res = self.email_error(error)
        if res :
            print(res)
        else :
            print(self.login_error(error))

        print("handling error with server ..")
