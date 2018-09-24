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

def newForum(name,creator):
    conn = sqlite3.connect('forums.db')
    cur = conn.cursor()
    now = datetime.datetime.now()
    currentDate =  now.strftime("%B %d, %Y")
    print(currentDate)
    cur.execute('INSERT INTO forums (name, creator,timestamp) VALUES (?, ?, ?)', [name, creator, currentDate])
    conn.commit()
    msg = "Record successfully added"
    #conn.close()
    return msg

#end of my classes******************************************************************
            #The following are variables that contain the queries that we will use within the upcomming methods
            #we grouped them here so that we can refer to them by name only and simplifiy the code, beside grouping them here
            # will simplify the process if we need to mofidy the query, view it, and refactoringself.
#***********************************************************************************
getUserid = 'select u.id username from users u where u.username = ?'
getAllForums = 'SELECT f.id id, f.name name, u.username username FROM forums f, users u where u.id = f.creator;'
getAspecificFourm = 'SELECT u.username username, f.name name, f.timestamp timestamp FROM forums f, users u where u.id = f.creator and f.id = ? order by f.timestamp;'
getAllThreadsWithinAforum = 'SELECT t.id id,t.title title ,u.username username,f.name,t.timestamp timestamp FROM forums f,users u,threads t where u.id = t.creator  and t.forumid = f.id and f.id = ? order by t.timestamp;'
getAspecificThread = 'select u.username username, tp.comment, tp.timestamp from users u,forums f, threadPosts tp, threads t where u.id = tp.creator and f.id = t.forumId and t.id = ? and tp.id = ? and f.id = ?'
#***********************************************************************************
#instantiate Auth class
basic_auth = Auth(app)
#***********************************************************************************
# Problems one and two, for route /forums and handling both GET and POST
@app.route('/forums',methods=['GET','POST'])
def showOrForums():
        conn = sqlite3.connect('forums.db')
        cur = conn.cursor()
        #use the query string that we created in the begining
        if request.method == 'GET':
            results = cur.execute(getAllForums).fetchall()
            #convert the result into JSON
            print(results)
            print('Anas') 
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
                print(data)
                forumName = data['name']
                newForum([forumName], (userId))
                return jsonify (data)
#***********************************************************************************
#Problems 3 and 4 for GET and POST on a specific forum_id
@app.route('/forums/<int:forum_Id>',methods=['GET','POST'])
def showThreadsWithinForum (forum_Id):
        #conn = sqlite3.connect('forums.db')
        cur = conn.cursor()
        #use the query string that we created in the begining
        if request.method == 'GET':
            intForumId = int(forum_Id)
            print (forum_Id)
            print (intForumId)
            results = cur.execute([getAllThreadsWithinAforum],(intForumId)).fetchall()
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


if __name__ == '__main__':
    app.run()
