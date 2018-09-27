#Anas Elhadidy 
#David 
#Jon 



import flask, click, sqlite3, sys ,datetime
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
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d
#***********************************************************************************   
def connectAndReturnCursor():
    conn = sqlite3.connect('forums.db', timeout=60) 
    conn.row_factory = dict_factory
    theCursor = conn.cursor()
    return theCursor 
#***********************************************************************************    
def forumExists(forum_id):
    cur = connectAndReturnCursor()
    data = cur.execute(checkForumId,forum_id).fetchone()
    cur.close()
    if data is none: 
      return 'NO'
    else: 
      return 'YES'
 #*********************************************************************************** 
def userExists(userName):
    cur = connectAndReturnCursor()
    data = cur.execute(checkUser, [userName]).fetchone()
    cur.close()
    if data: 
      return 'YES'
    else: 
      return 'NO'
 #*********************************************************************************** 
def getLastTread(): 
    cur = connectAndReturnCursor()
    theLastThread = cur.execute(lastThread).fetchone()
    #cur.close()
    thread_id = theLastThread["thread_id"]
    return thread_id
 #***********************************************************************************
def pushThread(threadTitle , userId, theadComment, timeStamp, thread_id, forum_id): 
    conn = sqlite3.connect('forums.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(insertThread,(threadTitle,userId,forum_id,timeStamp))
    conn.commit()
    cur.execute(insertThreadPost, (thread_id, userId, forum_id, timeStamp))
    conn.commit()
    cur.close()
    conn.close()
#***********************************************************************************    
def pushCommentToThread(userId, threadComment, timeStamp, thread_id):
    conn = sqlite3.connect('forums.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute(insertComment,(thread_id,userId,threadComment,timeStamp))
    conn.commit()
    cur.close()
    conn.close()  
 #***********************************************************************************  
def pushUser(userName):
    conn = sqlite3.connect('forums.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('insert into users (userName) values (?)',[userName])
    conn.commit()
    cur.close()
    conn.close()  
 #***********************************************************************************    
def updateUser(userName, password):
    conn = sqlite3.connect('forums.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    cur.execute('update users set password = ? where username = ?',(userName, password))
    conn.commit()
    cur.close()
    conn.close()
 #***********************************************************************************    
def fetchUserId(user): 
    cur = connectAndReturnCursor()
    userId = cur.execute(getUserid, [user]).fetchone()
    cur.close()
    id = userId["userId"]
    return str(id)
#***********************************************************************************
def newForum(name,creator):    
    cur = connectAndReturnCursor()
    now = datetime.datetime.now()
    currentDate =  now.strftime("%B %d, %Y")
    print(currentDate)
    cur.execute('INSERT INTO forums (name, creator,timestamp) VALUES (?, ?, ?)', [name, creator, currentDate])
    conn.commit()
    msg = "Record successfully added"
    cur.close()
    return msg

#end of my classes******************************************************************
            #The following are variables that contain the queries that we will use within the upcoming methods
            #we grouped them here so that we can refer to them by name only and simplify the code, beside grouping them here
            # will simplify the process if we need to modify the query, view it, and refactoring.
            
#****************************** Static Database Queries ***************************************
getUserid = 'select u.id userId from users u where u.username = ?'
getAllForums = 'SELECT f.id id, f.name name, u.username username FROM forums f, users u where u.id = f.creator;'
getAspecificFourm = 'SELECT u.username username, f.name name, f.timestamp timestamp FROM forums f, users u where u.id = f.creator and f.id = ? order by f.timestamp;'
getAllThreadsWithinAforum = 'SELECT t.id id,t.title title ,u.username username,f.name,t.timestamp timestamp FROM forums f,users u,threads t where u.id = t.creator  and t.forumid = f.id and f.id = ? order by t.timestamp;'
getAspecificThread = 'select u.username username, tp.comment,tp.timestamp from users u,forums f, threadPosts tp, threads t where u.id = tp.creator and f.id = t.forumId and tp.threadId = t.id and f.id = ? and t.id = ? ;'
checkThreadsName = 'select t.id from threads t, forums f where upper(t.title) = ? and t.forumId = f.id;'
getCommentsFromAThread = 'select u.username, tp.comment from users u , threadPosts tp, threads t, forums f where u.id = f.creator and f.id = t.forumId and t.id = tp.threadId and f.id = ? and t.id = ?;'
checkForumId = 'select t.id from forum where id = ?;'
checkUser = 'select id from users where userName = ?;'
lastThread = 'select max(id) thread_id from threads;'
insertThread = 'INSERT INTO threads(title,creator,forumid,timestamp) VALUES (?,?,?,?)' 
insertComment = 'insert into threadPosts(threadId, creator, comment, timeStamp) values (?,?,?,?);'
insertThreadPost = 'INSERT INTO threadPosts (threadId,creator,comment,timestamp) VALUES (?,?,?,?)'
#***********************************************************************************
#instantiate Auth class
basic_auth = Auth(app)
#***********************************************************************************
# Problems one and two, for route /forums and handling both GET and POST
@app.route('/forums',methods=['GET','POST'])
def getOrPostForums():
    cur = connectAndReturnCursor()
    if request.method == 'GET':
        results = cur.execute(getAllForums).fetchall()
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
        cur = connectAndReturnCursor()       
        if (forum_id):
            results = cur.execute(getAllThreadsWithinAforum,forum_id).fetchall()           
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
                if (forumExists == 'YES'): 
                    return 'HTTP 404 Not Found'
                else: 
                    now = datetime.datetime.now()
                    timeStamp = now.strftime("%A  %D %B %Y")   
                    conn = sqlite3.connect('forums.db', timeout=5) 
                    cur = conn.cursor()                    
                    thread_id = str(getLastTread())
                    conn.commit()
                    pushThread(threadTitle , userId, threadComment, timeStamp, thread_id, forum_id)
                    conn.close()
                    returnString = 'HTTP 201 Created Location header field set to /forums/' +  str(forum_id) + '/' +  str(thread_id)                     
                return   returnString  
#***********************************************************************************                
#Problems 5 and 6 for GET and POST on a specific forum_id and a specific thread_Id
@app.route('/forums/<forum_id>/<thread_id>',methods=['GET','POST'])
def showPostsWithinAThread(forum_id, thread_id):    
    if request.method == 'GET':   
        cur = connectAndReturnCursor()       
        if (forum_id and thread_id):
            results = cur.execute(getCommentsFromAThread,[forum_id, thread_id]).fetchall()           
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
                userId =  fetchUserId(user)
                payload =request.json
                threadComment=payload['comment']
                now = datetime.datetime.now()
                timeStamp = now.strftime("%A  %D %B %Y")   
                conn = sqlite3.connect('forums.db', timeout=5) 
                cur = conn.cursor()                    
                conn.commit()
                pushCommentToThread(userId, threadComment, timeStamp, thread_id)
                conn.close()
                result = 'comment:' +   threadComment                     
            return   jsonify(payload)
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
            return 'HTTP 200 OK'
         else: 
            return 'HTTP 404 Not Found if username does not exist.HTTP 409 Conflict if username does not match the current authenticated user.'
          
if __name__ == '__main__':
    app.run()
