import sqlite3
def connect():
    try :
        dbConn = sqlite3.connect('BotDB.sqlite')
        print('connected to database')
    except : dbConn = 'error'
    if dbConn != 'error' :
        curr = dbConn.cursor() #CURSOR 
        return (dbConn,curr)

def createTables():
    dbConn, curr = connect()
    curr.execute("CREATE TABLE IF NOT EXISTS Auth(email TEXT, password TEXT, ip TEXT)")
    print('auth table created')
    curr.execute("CREATE TABLE IF NOT EXISTS Code(code TEXT, ip TEXT)")
    print('code table created')
    dbConn.commit()

def addAuth(email, password, ip):
    dbConn, curr = connect()
    curr.execute("INSERT INTO Auth(email,password,ip) VALUES(?,?,?)",(email,password,ip))
    dbConn.commit()
    print("login infos added")
def addCode(code, ip):
    dbConn, curr = connect()
    curr.execute("INSERT INTO Code(code,ip) VALUES(?,?)",(code, ip))
    dbConn.commit()
    print("code added")

def getAuth():
    dbConn, curr = connect()
    cmd ="SELECT * FROM Auth"
    return curr.execute(cmd).fetchall()

def getCodes():
    dbConn, curr = connect()
    cmd = "SELECT * FROM Code"
    result = curr.execute(cmd)
    return result.fetchall()

#reateTables()
#addAuth('email@email','kgkjgjk','127.25.15')
#addCode('125748','1287.25.15')

getAuth()
getCodes()
