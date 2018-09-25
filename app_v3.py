import flask, click, sqlite3, sys ,datetime
from flask import g, request, jsonify, json, render_template
from flask_basicauth import BasicAuth

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

def newForum(name,creator):
    conn = sqlite3.connect('forums.db')
    cur = conn.cursor()
    now = datetime.datetime.now()
    currentDate =  now.strftime("%B %d, %Y")
    print(currentDate)
    cur.execute('INSERT INTO forums (name, creator,timestamp) VALUES (?, ?, ?)', [name, creator, currentDate])
    conn.commit()
    msg = "Record successfully added"
    #cur.close()
    #conn.close()
    return msg

#end of my classes******************************************************************
            #The following are variables that contain the queries that we will use within the upcoming methods
            #we grouped them here so that we can refer to them by name only and simplify the code, beside grouping them here
            # will simplify the process if we need to modify the query, view it, and refactoring.
            
#****************************** Static Database Queries ***************************************
getUserid = 'select u.id username from users u where u.username = ?'
getAllForums = 'SELECT f.id id, f.name name, u.username username FROM forums f, users u where u.id = f.creator;'
getAspecificFourm = 'SELECT u.username username, f.name name, f.timestamp timestamp FROM forums f, users u where u.id = f.creator and f.id = ? order by f.timestamp;'
getAllThreadsWithinAforum = 'SELECT t.id id,t.title title ,u.username username,f.name,t.timestamp timestamp FROM forums f,users u,threads t where u.id = t.creator  and t.forumid = f.id and f.id = ? order by t.timestamp;'
getAspecificThread = 'select u.username username, tp.comment,tp.timestamp from users u,forums f, threadPosts tp, threads t where u.id = tp.creator and f.id = t.forumId and tp.threadId = t.id and f.id = ? and t.id = ? ;'
#***********************************************************************************
#instantiate Auth class
basic_auth = Auth(app)
#***********************************************************************************
# Problems one and two, for route /forums and handling both GET and POST
@app.route('/forums',methods=['GET','POST'])
def getOrPostForums():
    conn = sqlite3.connect('forums.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    if request.method == 'GET':
        results = cur.execute(getAllForums).fetchall()
        return jsonify(results)        
    if request.method == 'POST':
                #get username and password from Authorization header
        user = request.authorization.username
        print(user)
        userId = cur.execute([getUserid], (user)).fetchall()
        password = request.authorization.password
                #authenticate user
        auth = Auth()
        validUser = len(auth.check_credentials(user,password))
        if  validUser <= 2:
            return 'invalid login'
        elif validUser > 2:
            data = request.get_json()
            forumName = data['name']
            newForum([forumName], (userId))
            return jsonify (data)

#***********************************************************************************
#Problems 3 and 4 for GET and POST on a specific forum_id
@app.route('/forums/',methods=['GET','POST'])
def showThreadsWithinForum():    
    if request.method == 'GET':
        query_parameters = request.args
        forum_id  = query_parameters.get('forum_id')
        thread_id = query_parameters.get('thread_id')     
        conn = sqlite3.connect('forums.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()       
        if (forum_id and not thread_id):
            idFilter = forum_id 
            results = cur.execute(getAllThreadsWithinAforum,idFilter).fetchall()           
        elif(forum_id and thread_id):
            idFilter = forum_id 
            threadFilter = thread_id
            results = cur.execute(getAspecificThread,(idFilter,threadFilter)).fetchall()          
        else:
            return 'HTTP 404 Not Found'             
        return jsonify(results)
        
    if request.method == 'POST':
                    #get username and password from Authorization header
            user = request.authorization.username
            print(user)
            #userId = cur.execute(getUserid, user).fetchall()
            password = request.authorization.password
                    #authenticate user
            auth = Auth()
            validUser = len(auth.check_credentials(user,password))
            if  validUser <= 2:
                return 'invalid login'
            elif validUser > 2:
                data = request.get_json()
                forumName = data['name']
                newThread(forumName, 1)
                return jsonify (data)
'''
#***********************************************************************************
#Problems 5 and 6 for GET and POST on a specific forum_id and a specific thread_Id
@app.route('/forums/<int:forum_Id>/<thread_Id>',methods=['GET','POST'])
def showThreadsWithinForum (forum_Id):
        conn = sqlite3.connect('forums.db')
        cur = conn.cursor()
        #use the query string that we created in the begining
        if request.method == 'GET':
            intForumId = int(forum_Id)
            intThreadId = int(thread_Id)
            print (forum_Id)
            print (intForumId)
            results = cur.execute([getAspecificThread],(intForumId,intThreadId)).fetchall()
            #convert the result into JSON
            return jsonify(results)
        if request.method == 'POST':
                    #get username and password from Authorization header
            user = request.authorization.username
            print(user)
            #userId = cur.execute(getUserid, user).fetchall()
            password = request.authorization.password
                    #authenticate user
            auth = Auth()
            validUser = len(auth.check_credentials(user,password))
            if  validUser <= 2:
                return 'invalid login'
            elif validUser > 2:
                data = request.get_json()
                forumName = data['name']
                newThread(forumName, 1)
                return jsonify (data)
'''
if __name__ == '__main__':
    app.run()
