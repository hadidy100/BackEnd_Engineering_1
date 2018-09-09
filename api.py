import flask
from flask import request, jsonify, json, render_template
from flaskext.mysql import MySQL
from flask_basicauth import BasicAuth

app = flask.Flask(__name__)

#mysql configuration
mysql = MySQL()
mysql.init_app(app)
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = 'FLASK'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config["DEBUG"] = True

#create all of my classes here*******************************************************

#authentication class
#subclass of BasicAuth, with check_credentials function overriden
class Auth(BasicAuth):
    def check_credentials(self,username,password):
        if username == 'david' and password == 'password':
            return True
        else:
            return False
#end of my classes******************************************************************

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
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM forums")
        data = cursor.fetchall()
        payload = []
        for result in data:
            content = {
                'id': result[0],
                'name': result[1],
                'creator':result[2]
            }
            payload.append(content)
        return jsonify(payload)
    elif request.method == 'POST':
        return 'new forum'
        #enter new forum into database

#********************************************************
#*******************end problem 1************************



#********************problem2****************************
#********************************************************
@app.route('/forums',methods=['POST'])
@basic_auth.required
@basic_auth.challenge
def createForum():
    signedIn = basic_auth.check_credentials('david','pass')
    return str(signedIn)

#********************************************************
#*********************end problem 2**********************


app.run()
