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

#******************************************************

#instantiate Auth class
basic_auth = Auth(app)


#*******************HOMEPAGE****************************
#*******************************************************
#initial default page localhost:5000 or 127.0.0.1:5000
@app.route('/', methods=['GET'])
def home():
    return render_template('index.html')

#*******************END HOMEPAGE************************
#*******************************************************


#*********************problem 1*************************
#*******************************************************
#localhost:5000/forums
#will return available discussion forums if any exist in MYSQL
#MySQL database: FLASK, table: forums, columns: id, name, creator

@app.route('/forums',methods=['GET'])
def showForums():
    if request.method == 'GET':
        conn = sqlite3.connect('forums.db')
        conn.row_factory = dict_factory
        cur = conn.cursor()
        results = cur.execute('SELECT * FROM forums;').fetchall()

        return jsonify(results)
#********************************************************
#*******************end problem 1************************



#********************problem2****************************
#********************************************************

@app.route('/forums',methods=['POST'])
def createForum():

    #get username and password from Authorization header
    user = request.authorization.username
    password = request.authorization.password
    
    #authenticate user
    auth = Auth()
    validUser = len(auth.check_credentials(user,password))

    if  validUser <= 2:
        return 'invalid login'
    elif validUser > 2:
        #pull forum name provided by user
        data = request.get_json()
        forumName = data['name']
        
        #call function to insert new forum into database
        enter = newForum(forumName,user)
        return enter
        
#********************************************************
#*********************end problem 2**********************

#place in an if statement to silence flask init_db, when database script is ran
if __name__ == '__main__':
    app.run()
