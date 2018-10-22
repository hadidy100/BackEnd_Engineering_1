#Anas Elhadidy 
#David 
#Jon  
import flask, click, sqlite3, sys ,datetime, uuid
from flask import g, request, jsonify, json, render_template
from flask_basicauth import BasicAuth
from datetime import date
from datetime import time


app = flask.Flask(__name__)
app.debug = True
#create all of my classes here*******************************************************
#authentication class
#subclass of BasicAuth, with check_credentials function overwritten
class Auth(BasicAuth):
    def check_credentials(self,username,password):
        query = "SELECT username,password,id FROM users WHERE"
        to_filter = []
        if username:
            query += ' username=? AND'
            to_filter.append(username)
        if password:
            query += ' password=? ;'
            to_filter.append(password)
        conn = sqlite3.connect('forums.db')
        cur = conn.cursor()
        results = cur.execute(query, to_filter).fetchall()
        return str(results[0])
#Method to create a dictionary to map the column name to a value, where the column name will be fetched 
#from the cursor that we get back from the database connection (cursor.description)
# get the database forums.db using sqlite3
#***********************************************************************************   
#@app.cli.command()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql',mode='r') as f: 
            db.cursor().executescript(f.read())
        #db.commit()
#***********************************************************************************   
def get_db():
    DATABASE = 'forums.db'
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db
#***********************************************************************************   
#allow the command line to run .sql script
# by calling this init_db() function
# console command: flask init_db()
#***********************************************************************************   
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#***********************************************************************************   
def connectAndReturnCursor(DATABASE):  
    theConnection = sqlite3.connect(DATABASE, timeout=5) 
    theConnection.row_factory = dict_factory
    theCursor = theConnection.cursor()
    connectionObject = {}
    connectionObject["cursor"] = theCursor
    connectionObject["connection"] = theConnection
    return connectionObject 
#*************************************************************************************    
def searchAllShards(formId):
    cur = connectAndReturnCursor()
    shard0 = ('shard_0.db',)
    shard1 = ('shard_1.db',)
    shard2 = ('shard_2.db',)
    cur.execute(attachShard0, shard0)
    cur.execute(attachShard1, shard1)
    cur.execute(attachShard2, shard2)
    cur
#*************************************************************************************
def newForum(name,creator):    
    connObject = connectAndReturnCursor('forums.db')
    cur = connObject["cursor"]
    conn = connObject["connection"]
    now = datetime.datetime.now()
    currentDate =  now.strftime("%B %d, %Y")
    print(currentDate)
    cur.execute(insertForums , [name, creator, currentDate])
    conn.commit()    
    msg = "Record successfully added"
    cur.close()
    conn.close()
    return msg
#************************************************************************************* 
def pushThread(shardNumber,threadTitle , userId, theadComment, timeStamp, thread_id, forum_id): 
    connObject = connectAndReturnCursor(shardNumber)
    conn = connObject["connection"]
    cur = connObject["cursor"]
    cur.execute(insertThread,(thread_id,threadTitle,userId,forum_id,timeStamp))
    conn.commit()
    cur.execute(insertThreadPost, (thread_id, userId, theadComment, timeStamp))
    conn.commit()
    cur.close()
    conn.close()
#***********************************************************************************    
def pushCommentToThread(shardNumber, userId, threadComment, timeStamp, thread_id):
    connObject = connectAndReturnCursor(shardNumber)
    conn = connObject["connection"]
    cur = connObject["cursor"]
    cur.execute(insertComment,(thread_id,userId,threadComment,timeStamp))
    conn.commit()
    cur.close()
    conn.close()  
 #***********************************************************************************  
def pushUser(userName):
    conn = sqlite3.connect('shard_0.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('insert into users (userName) values (?)',[userName])
    conn.commit()
    cur.close()
    conn.close()  
 #***********************************************************************************    
def updateUser(userName, password):
    conn = sqlite3.connect('shard_0.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('update users set password = ? where username = ?',(userName, password))
    conn.commit()
    cur.close()
    conn.close()
 #***********************************************************************************    
def fetchUserId(user): 
    connObject = connectAndReturnCursor('forums.db')
    cur = connObject["cursor"]
    conn = connObject["connection"]
    userId = cur.execute(getUserid, [user]).fetchone()
    cur.close()
    conn.close()
    id = userId["userId"]
    return str(id)
#*************************************************************************************
def forumExists(forum_id):
    connObject = connectAndReturnCursor('forums.db')
    conn = connObject["connection"]
    cur = connObject["cursor"]
    data = cur.execute(checkForumId,forum_id).fetchone()
    cur.close()
    conn.close()
    if data: 
      return 'YES'
    else: 
      return 'NO'
 #*********************************************************************************** 
def createGUID(): 
    sqlite3.register_converter('GUID', lambda b: uuid.UUID(bytes_le=b))
    sqlite3.register_adapter(uuid.UUID, lambda u: buffer(u.bytes_le))
    GUID = uuid.uuid4() 
    return GUID 
#*************************************************************************************  
def getModuluOfLastDigit(threadId): 
    #get the last digit of the string and convert it to an integer with an assumption that it came in as base 16 as in HEX
    convertedInteger = int(threadId[len(threadId)-1],16) 
    #get the modulus of the previous integer by 3
    moduloHexOn3 = convertedInteger % 3
    return moduloHexOn3  # remember that this is returned to the caller as an integer 
#***********************************************************************************  
def attachAllDatabases(DATABASE):
#initially use forums database, and then attach the other database to it
    connObject = connectAndReturnCursor('forums.db')
    cur = connObject["cursor"]
    conn = connObject["connection"]
    commands = cur.execute("attach database 'forums.db' as 'db1' ")
    commands = cur.execute(attachShard0,['shard_0.db' , 'db2'])
    commands = cur.execute(attachShard1,['shard_1.db' , 'db3'])
    commands = cur.execute(attachShard2,['shard_2.db' , 'db4'])
    return connObject   
            
#****************************** Static Database Queries ***************************************
            #The following are variables that contain the queries that we will use within the upcoming methods
            #we grouped them here so that we can refer to them by name only and simplify the code, beside grouping them here
            # will simplify the process if we need to modify the query, view it, and refactoring.

insertForums = 'INSERT INTO forums (name, creator,timestamp) VALUES (?, ?, ?);'
getUserid = 'select u.id userId from users u where u.username = ?'
getAllForums = 'SELECT f.id id, f.name name, u.username username FROM forums f, users u where u.id = f.creator;'
#***********************************************************************************
#long query for selecting all thread from all shards using union all
getAllThreadsWithinAforum = ( 
    'select ' 
       't.id id, ' 
       't. title title, ' 
       'u.username username, ' 
       'f.name name, ' 
       't.timestamp timestamp ' 
    'from ' 
        'db1.forums f, ' 
        'db1.users u ,' 
        'db2.threads t ' 
    'where ' 
        'u.id = t.creator and ' 
        't.forumid = f.id and ' 
        'f.id = ? ' 
    ' union all ' 
    ' select ' 
       't.id id, ' 
       't. title title, ' 
       'u.username username, ' 
       'f.name name, ' 
       't.timestamp timestamp ' 
    'from ' 
        'db1.forums f, ' 
        'db1.users u ,' 
        'db3.threads t ' 
    'where ' 
        'u.id = t.creator and ' 
        't.forumid = f.id and ' 
        'f.id = ? ' 
    ' union all ' 
    ' select ' 
       't.id id, ' 
       't. title title, ' 
       'u.username username, ' 
       'f.name name, ' 
       't.timestamp timestamp ' 
    'from ' 
        'db1.forums f, ' 
        'db1.users u ,' 
        'db4.threads t ' 
    'where ' 
        'u.id = t.creator and ' 
        't.forumid = f.id and ' 
        'f.id = ? ' 
      
    'order by 5; ')
#***********************************************************************************    
#long query for selecting all comments from all shards using joins based on the dynamic attachments of the databases
getCommentsFromAThread = (
    'select '
        ' u.username, ' 
        ' tp.comment ' 
    ' from ' 
        ' users u , ' 
        ' threadPosts tp, '
        ' threads t, ' 
        ' forums f ' 
    ' where ' 
        ' u.id = f.creator and ' 
        ' f.id = t.forumId and ' 
        ' t.id = tp.threadId and ' 
        ' f.id = ? and t.id = ?;'
)
#***********************************************************************************
checkForumId = 'select id from forums where id = ?;'
insertThread = 'INSERT INTO threads(id,title,creator,forumid,timestamp) VALUES (?,?,?,?,?)' 
insertComment = 'insert into threadPosts(threadId, creator, comment, timeStamp) values (?,?,?,?);'
insertThreadPost = 'INSERT INTO threadPosts (threadId,creator,comment,timestamp) VALUES (?,?,?,?)'
attachShard0 = 'ATTACH DATABASE ? AS ?'
attachShard1 = 'ATTACH DATABASE ? AS ?'
attachShard2 = 'ATTACH DATABASE ? AS ?' 
#***********************************************************************************
#instantiate Auth class  
basic_auth = Auth(app)
initialize_DB = init_db()
#initially use forums database, and then attach the other database to it

#************************ ROUTES ***************************************************
@app.route('/forums',methods=['GET','POST'])
def getOrPostForums():
    connObject = connectAndReturnCursor('forums.db')
    cur = connObject["cursor"]
    conn = connObject["connection"]
    if request.method == 'GET': 
        results = cur.execute(getAllForums).fetchall()
        cur.close()
        conn.close()
        return jsonify(results)        
    if request.method == 'POST':
        user = request.authorization.username
        userId = int(fetchUserId(user))
        password = request.authorization.password
        auth = Auth()
        validUser = len(auth.check_credentials(user,password))
        if  validUser <= 2:
            return 'invalid login'
        elif validUser > 2:
            data = request.get_json()
            forumName = data['name']
            newForum(forumName, (userId))
            return jsonify (data)
#***********************************************************************************
#Problems 3 and 4 for GET and POST on a specific forum_id
@app.route('/forums/<forum_id>',methods=['GET','POST'])
def showThreadsWithinForum(forum_id):    
    if request.method == 'GET':   
        if (forum_id):
            connObject = attachAllDatabases('forums.db')
            cur = connObject["cursor"]
            conn = connObject["connection"]
            #This is where the big query that does a UNION ALL is utilized
            results = cur.execute(getAllThreadsWithinAforum,[forum_id,forum_id, forum_id]).fetchall() 
            cur.close()
            conn.close()           
        else:
            return 'HTTP 404 Not Found, Please check the forum ID'             
        return jsonify(results)        
    if request.method == 'POST':
            user = request.authorization.username
            password = request.authorization.password
            auth = Auth()
            validUser = len(auth.check_credentials(user,password))
            if  validUser <= 2:
                return 'invalid login'
            elif validUser > 2:
                userId =  fetchUserId(user) 
                payload =request.json
                threadTitle=payload['title']
                threadComment=payload['text']
                flaskUpper =  threadTitle.upper()
                
                if (forumExists(forum_id) == 'NO'): 
                    return 'HTTP 405, this does not exit'
                else: 
                    now = datetime.datetime.now()
                    threadId = str(createGUID())
                    shardNumber = str(getModuluOfLastDigit(threadId) )
                    timeStamp = now.strftime("%A  %D %B %Y")  
                    shardName = 'shard_' + shardNumber + '.db' 
                    pushThread(shardName ,threadTitle , userId, threadComment, timeStamp, threadId, forum_id)
                    returnString = 'HTTP 201 Created Location header field set to /forums/' +  str(forum_id) + '/' +  threadId
                return   returnString  
#***********************************************************************************                
#Problems 5 and 6 for GET and POST on a specific forum_id and a specific thread_Id
@app.route('/forums/<forum_id>/<thread_id>',methods=['GET','POST'])
def showPostsWithinAThread(forum_id, thread_id):    
    if request.method == 'GET': 
        if (forum_id and thread_id):
            connObject = connectAndReturnCursor('forums.db')
            conn = connObject["connection"]
            cur = connObject["cursor"]
            shardNumber = str(getModuluOfLastDigit(thread_id) ) 
            shardName = 'shard_' + shardNumber + '.db' 
            aliase = 'db' + shardNumber        
            cur.execute('attach database ? as ?;', [shardName, aliase])           
            results = cur.execute(getCommentsFromAThread,[forum_id, thread_id]).fetchall()  
            cur.close()
            conn.close()            
        else:
            return 'HTTP 404 Not Found, Please check the forum ID'             
        return jsonify(results)        
    if request.method == 'POST':
        if (forum_id and thread_id):        
            user = request.authorization.username
            password = request.authorization.password
            auth = Auth()
            validUser = len(auth.check_credentials(user,password))
            if  validUser <= 2:
                return 'invalid login'
            elif validUser > 2:
                shardNumber = str(getModuluOfLastDigit(thread_id) ) 
                shardName = 'shard_' + shardNumber + '.db' 
                aliase = 'db' + shardNumber 
                userId =  fetchUserId(user)
                payload =request.json
                threadComment=payload['comment']
                now = datetime.datetime.now()
                timeStamp = now.strftime("%A  %D %B %Y") 
                pushCommentToThread(shardName, userId, threadComment, timeStamp, thread_id)
                result = 'comment:' +   threadComment                     
            return jsonify(payload)
        else: 
           return 'HTTP error 499 :you did not provide a completed forum_id or thread id'
#***********************************************************************************
@app.route('/users',methods=['GET','POST','PUT'])
def createUser():
    if request.method == 'GET': 
        return 'HTTP 499, You can not make a get request to this route'
    elif  request.method == 'POST': 
       payload = request.json
       userName = payload['userName']
       if (userExists(userName) == 'YES'):
          return 'HTTP 409 Conflict if username already exists'
       else: 
          pushUser(userName)
          return 'HTTP 201 Created'
    elif  request.method == 'PUT':
         payload = request.json
         userName = payload['userName']
         password = payload['password']
         if (userExists(userName) == 'YES'):
            updateUser(userName,password)
            return jsonify(payload)
         else: 
            return 'HTTP 404 Not Found if username does not exist.HTTP 409 Conflict if username does not match the current authenticated user.'
          
if __name__ == '__main__':
    app.run()
