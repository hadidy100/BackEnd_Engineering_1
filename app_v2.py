import flask, click, sqlite3, sys
from flask import g, request, jsonify, json, render_template
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)

# get the database forums.db using sqlite3
def get_db():
    DATABASE = 'forums.db'
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def connectToDatabaseAndReturnCursor():
    conn = sqlite3.connect('forums.db')
    cur = conn.cursor()
    return cur



#allow the command line to run .sql script
# by calling this init_db() function
# console command: flask init_db()
@app.cli.command()
def init_db():
    with app.app_context():
        db = get_db()
        with app.open_resource('init.sql',mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

#sqlite3 setup configuration
def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

#create all of my classes here*******************************************************

#authentication class
#subclass of BasicAuth, with check_credentials function overwritten
class Auth(BasicAuth):
    def check_credentials(self,username,password):
        query = "SELECT username,password FROM users WHERE"
        to_filter = []
        if username:
            query += ' username=? AND'
            to_filter.append(username)
        if password:
            query += ' password=? ;'
            to_filter.append(password)

        conn = sqlite3.connect('forums.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        results = cur.execute(query, to_filter).fetchall()
        return str(results[0])
#end of my classes******************************************************************

#backend functions*************************************
def newForum(name,creator):
    conn = sqlite3.connect('forums.db')
    conn.execute("INSERT INTO forums(name,creator) VALUES (?,?)",(name,creator))
    conn.commit()
    msg = "Record successfully added"
    conn.close()
    return msg
#**********************************************************
def checkForums (forumName):
    theExistingForumId = cur.execute('select id from forums where name = ?',forumName)
    return theExistingForumId
#**********************************************************
#instantiate Auth class
basic_auth = Auth(app)

#*******************HOMEPAGE****************************
#initial default page localhost:5000 or 127.0.0.1:5000
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')
#*******************END HOMEPAGE************************


#*********************problem 1 and 2 *************************
#localhost:5000/forums
#will return available discussion forums if any exist in the database
@app.route('/forums',methods=['GET','POST'])
def showOrCreateForums():
    # get method
    if request.method == 'GET':
        mu = 'Amnana'
    # cur = connectToDatabaseAndReturnCursor()
    #results = cur.execute('SELECT * FROM forums;').fetchall()
    #return jsonify(results)
    #**********************************************************
    #post method
    #If the check_credentials method did not return a username and password, then user is not authenticated. else then the user is authenticated
    #get the username and password form the request
    #check first if such a forum already exists, if it does, then throw an error, else create it and push it in the database
    #If the cursor returned at least one row, then the forumexists, else then it had never been created before.
    #if the cursor had one row with that forum name then it alreay  exits, so we should not allow for creating it
    #call function to insert new forum into database

    if request. method == 'POST':
        cur = connectToDatabaseAndReturnCursor()
        user = request.authorization.username
        password = request.authorization.password
        auth = Auth()
        validUser = len(auth.check_credentials(user.password))
        if validUser <=2:
            return 'invalid loging, or no such user exists, please try to login with the correct credntials '
        elif validUser >2:
            cur = connectToDatabaseAndReturnCursor()
            postedRequest = request.get_json()
            forumName = postedRequest['name']
            result = checkForums(forumName)
            atLeastOneRow = cur.fethchone()
            if atLeastOneRow != None:
                    return 'HTTP 409 Conflict if forum already exists'
            else:
                    theUsersName = postedRequest['username']
                    theUsersId = cur.execute ('select id from users where username = theUsersName')
                    theTimeStamp = DATETIME('now','localtime')
                    cur.execute('insert into forums (name,creator,timestamp) values (forumName, theUsersId,theTimeStamp')
                    enter = newForum(forumName,user)
                    return enter
#*********************end problem 1 and 2 *************************
#place in an if statement to silence flask init_db, when database script is ran
if __name__ == '__main__':
    app.run()
