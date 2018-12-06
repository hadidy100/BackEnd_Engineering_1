#Anas Elhadidy 
#Jon Sumarto
#David Toledo Viveros
#Utilizing scylla DB and the cassandra framework, this API utilizes the previously forum application that #we built but using nosql database, for best result for horizontal scalability 
#The code creates the keyspace, index, and the tables in one script and then listens on port 5000 for #flask requests


import flask, click, sqlite3, sys ,datetime, uuid
from flask import g, request, jsonify, json, render_template
from flask_basicauth import BasicAuth
from datetime import date
from datetime import time
from cassandra.cluster import Cluster

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
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsdb'    
    session.execute(""" CREATE KEYSPACE IF not EXISTS %s with replication = {'class': 'SimpleStrategy', 'replication_factor': '1'} """ % theKeyspace)
    session.execute(""" USE forumsdb """)
    session.execute (""" drop table if exists UserForumThreadPosts """)
    session.execute(""" create table if not exists UserForumThreadsPosts 
                    (
                    userId int, 
                    threadId int, 
                    forumID int, 
                    postID int,
                    userName text, 
                    password text,
                    forumTitle text, 
                    forumCreator text, 
                    forumTimeStamp timestamp, 
                    threadTitle text, 
                    threadCreator text, 
                    threadTimeStamp timestamp,
                    postCreator text, 
                    postComment text, 
                    postTimeStammp timestamp, 
                    primary key (userId, threadId, forumId, postID))
                    """)
    session.execute(""" CREATE INDEX IF NOT EXISTS username_index on forumsdb.userforumthreadsposts (username) """ )

    session.execute(""" insert into UserForumThreadsPosts 
		    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (1,
                    1,
                    1,
                    1,
                    'david',
                    'password',
                    'redis',
                    'david',
                    toTimeStamp(now()),
                    'help',
                    'david',
                    toTimeStamp(now()),
                    'david',
                    'I can not start Redis, I ping to the IP address, but I get no response', 
                     toTimeStamp(now()))

                    """ ) 

    
    session.execute(""" insert into UserForumThreadsPosts 
		    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (2,
                    1,
                    2,
                    2,
                    'anas',
                    'password',
                    'redis',
                    'david',
                    toTimeStamp(now()),
                    'Has anyone heard of Edis?',
                    'david',
                    toTimeStamp(now()),
                    'anas',
                    'I keep hearing about this Edis, what exactly is it? And how different is it from Redis?', 
                     toTimeStamp(now()))   
                   """)

    session.execute(""" insert into UserForumThreadsPosts 
		    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (2,
                    1,
                    3,
                    3,
                    'anas',
                    'password',
                    'redis',
                    'jon',
                    toTimeStamp(now()),
                    'Has anyone heard of Edis?',
                    'david',
                    toTimeStamp(now()),
                    'anas',
                    'According to this website, https://dbdb.io, Edis an an Erlang re-implementation of Redis', 
                     toTimeStamp(now()))                          
		    """ ) 

    session.execute(""" insert into UserForumThreadsPosts 
                    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (2,
                    4,
                    2,
                    5,
                    'jon',
                    'password',
                    'mongodb',
                    'david',
                    toTimeStamp(now()),
                    'mongodb vs hadoop',
                    'anas',
                    toTimeStamp(now()),
                    'david',
                    'Can anyone please tell what is the difference between mangoDB and Hadoop? ', 
                     toTimeStamp(now()))

                    """ ) 

    session.execute(""" insert into UserForumThreadsPosts 
                    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (2,
                    4,
                    2,
                    6,
                    'jon',
                    'password',
                    'mongodb',
                    'jon',
                    toTimeStamp(now()),
                    'mongodb vs hadoop',
                    'anas',
                    toTimeStamp(now()),
                    'jon',
                    'I have the same question, you took the words out of my mouth! ', 
                     toTimeStamp(now()))

                    """ )                     

    session.execute(""" insert into UserForumThreadsPosts 
                    (userId,
                    threadId,
                    forumId,
                    postId,
                    userName,
                    password,
                    forumTitle,
                    forumCreator,
                    forumTimeStamp,
                    threadTitle,
                    threadCreator,
                    threadTimeStamp,
                    postCreator,
                    postComment,
                    postTimeStammp
                    ) 
                    values 
                    (3,
                    5,
                    3,
                    7,
                    'jon',
                    'password',
                    'Oracle DB',
                    'jon',
                    toTimeStamp(now()),
                    'Price',
                    'anas',
                    toTimeStamp(now()),
                    'jon',
                     'Why would any enterprise chooses to use Oracle instead of mySql is byond me, I mean it is a lot more expesive, and I do not see any performance or capability issues, thoughts? Anyone? ', 
                     toTimeStamp(now()))

                    """ )                       
                                        
                    
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
def connectAndReturnCursor():  
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'   
    connectionObject = {}
    connectionObject["cursor"] = session
    connectionObject["keyspace"] = theKeyspace
    return connectionObject 
#*************************************************************************************    
def newForum(name,creator):    
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'
    now = datetime.datetime.now()
    currentDate =  now.strftime("%B %d, %Y")
    print(currentDate)
    session.execute(insertForums , [name, creator, currentDate])    
    msg = "Record successfully added"
    return msg
#************************************************************************************* 
def pushThread(threadTitle , userId, theadComment, timeStamp, thread_id, forum_id): 
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'
    session.execute(insertThread,(thread_id,threadTitle,userId,forum_id,timeStamp))
    cur.execute(insertThreadPost, (thread_id, userId, theadComment, timeStamp))
    
#***********************************************************************************    
def pushCommentToThread( userId, threadComment, timeStamp, thread_id):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'
    session.execute(insertComment,(thread_id,userId,threadComment,timeStamp))
  
 #***********************************************************************************  
def pushUser(userName):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'
    conn.row_factory = dict_factory
    session.execute('insert into users (userName) values (?)',[userName])

 #***********************************************************************************    
def updateUser(userName, password):
   cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    theKeyspace = 'forumsDB'
    session.execute('update users set password = ? where username = ?',(userName, password))

 #***********************************************************************************    
def fetchUserId(user): 
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    session.execute(""" USE forumsdb """)
    userId = session.execute('select  userId from forumsdb.userforumthreadsposts where username = (%s)', ["user"])
    #cur.close()
    #conn.close()
    id = userId["userId"]
    return id
#*************************************************************************************
def forumExists(forum_id):
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    session.execute(""" USE forumsdb """)
    data = cur.execute(checkForumId,forum_id)
    if data: 
      return 'YES'
    else: 
      return 'NO'
 #*********************************************************************************** 
def userExists(userName):
   cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    session.execute(""" USE forumsdb """)
    data = session.execute(checkUser, [userName])

    if data: 
      return 'YES'
    else: 
      return 'NO'
 #*********************************************************************************** 
def createGUID():  #not needed any more
   
    GUID = uuid.uuid4() 
    return GUID 

#****************************** Static Database Queries ***************************************
            #The following are variables that contain the queries that we will use within the upcoming methods
            #we grouped them here so that we can refer to them by name only and simplify the code, beside grouping them here
            # will simplify the process if we need to modify the query, view it, and refactoring.

insertForums = 'INSERT INTO forumsdb.userforumthreadsposts (name, creator,timestamp) VALUES (?, ?, ?);'
getUserid = 'select  userId from forumsdb.userforumthreadsposts where username = (%s)'
getAllForums = 'SELECT  forumID, forumTitle, username FROM forumsdb.userforumthreadsposts'
#***********************************************************************************

getAllThreadsWithinAforum = ( 
    'select ' 
       'threadId, ' 
       'threadTitle, ' 
       'userName, ' 
       'forumTitle, ' 
       'threadTimeStamp ' 
    'from ' 
        'forumsdb.userforumthreadsposts' 
 )    
#***********************************************************************************    
#long query for selecting all comments from all shards using joins based on the dynamic attachments of the databases
getCommentsFromAThread = (
    'select '
        ' userName, ' 
        ' postComment ' 
    ' from ' 
        ' forumsdb.userforumthreadsposts ' 
    ' where ' 
        ' forumID = ? and threadId = ?;'
)
#***********************************************************************************
checkForumId = 'select forumID from forumsdb.userforumthreadsposts where forumID = ?;'
insertThread = 'INSERT INTO forumsdb.userforumthreadsposts(userId,threadTitlre,threadCreator,forumid,threadtimestamp) VALUES (?,?,?,?,?)' 
insertComment = 'insert into forumsdb.userforumthreadsposts(threadId, creator, comment, timeStamp) values (?,?,?,?);'
insertThreadPost = 'INSERT INTO forumsdb.userforumthreadsposts (threadId,creator,comment,timestamp) VALUES (?,?,?,?)'
checkUser = 'select id from users where userName = ?;'
#***********************************************************************************
#instantiate Auth class  
basic_auth = Auth(app)
initialize_DB = init_db()
#initially use forums database, and then attach the other database to it

#************************ ROUTES ***************************************************
@app.route('/forums',methods=['GET','POST'])
def getOrPostForums():
    cluster = Cluster(['172.17.0.2'])
    session = cluster.connect()
    session.execute(""" USE forumsdb """)
    if request.method == 'GET': 
        results = session.execute(getAllForums)         
        return jsonify (list(results))
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
            cluster = Cluster(['172.17.0.2'])
            session = cluster.connect()
            session.execute(""" USE forumsdb """)
            #This is where the big query that does a UNION ALL WAS utilized in the past 
            results = session.execute(getAllThreadsWithinAforum,[forum_id,forum_id, forum_id])
                  
        else:
            return 'HTTP 404 Not Found, Please check the forum ID'             
        return jsonify (list(results))      
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
                    threadId = getMaxthradId()+1
             
                    timeStamp = now.strftime("%A  %D %B %Y")  
                  
                    pushThread(threadTitle , userId, threadComment, timeStamp, threadId, forum_id)
                    returnString = 'HTTP 201 Created Location header field set to /forums/' +  str(forum_id) + '/' +  threadId
                return   returnString  
#***********************************************************************************                
#Problems 5 and 6 for GET and POST on a specific forum_id and a specific thread_Id
@app.route('/forums/<forum_id>/<thread_id>',methods=['GET','POST'])
def showPostsWithinAThread(forum_id, thread_id):    
    if request.method == 'GET': 
        if (forum_id and thread_id):
            cluster = Cluster(['172.17.0.2'])
            session = cluster.connect()
            session.execute(""" USE forumsdb """)                      
            results = session.execute(getCommentsFromAThread,[forum_id, thread_id])                   
        else:
            return 'HTTP 404 Not Found, Please check the forum ID'             
        return jsonify(list(results))        
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
                pushCommentToThread( userId, threadComment, timeStamp, thread_id)
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
            return 'HTTP 409 Conflict .'
          
if __name__ == '__main__':
    app.run()
