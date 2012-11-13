import os
import datetime
from flask import Flask
from flask import render_template
from flask import flash, redirect, url_for, request, make_response
#from flask.ext.pymongo import PyMongo
from pymongo import Connection

#Create an instance of flask
app = Flask(__name__)

#Build the variables that use the assigned environment variables
HOST = os.environ['OPENSHIFT_MONGODB_DB_HOST']
PORT = int(os.environ['OPENSHIFT_MONGODB_DB_PORT'])
DB_USER = os.environ['OPENSHIFT_MONGODB_DB_USERNAME']
DB_PWD = os.environ['OPENSHIFT_MONGODB_DB_PASSWORD']
DB_NAME = 'vetprops' #data base name
'''
app.config['MDB_HOST'] = HOST
app.config['MDB_PORT'] = PORT
app.config['MDB_USERNAME'] = DB_USER
app.config['MDB_PASSWORD'] = DB_PWD
app.config['MDB_DBNAME'] = DB_NAME
#mdb = PyMongo(app, config_prefix='MDB') #Create instance of PyMongo object
'''
app.config['PROPAGATE_EXCEPTIONS'] = True



#Setup the database connections for OpenShift 
muri = "mongodb://" + DB_USER + ":" + DB_PWD + "@" + HOST + ":" + str(PORT)
mconn = Connection(muri)
db = mconn[DB_NAME]

TITLE = "Vet Props" 

@app.template_filter("frmdate")
def frmDate(s):
    d = s.strftime("%m/%d/%Y %H:%M:%S")
    return d

@app.route("/")
@app.route("/index")
def index():
 
    return render_template("index.html", title = TITLE)

@app.route("/insert", methods=["GET","POST"])
def insert():
    poster = request.form['poster']
    service = request.form['service']
    message = request.form['message']
    i = {"name":poster.strip(),"service":service.strip(),"message":message.strip(),"timestamp":datetime.datetime.utcnow()}
    db.post.insert(i)
    
    #result = mdb.db.post.find().sort('timestamp',-1)
    #return render_template("view.html", result = result, title = TITLE)
    return redirect("/view")
    
@app.route("/view", methods=["GET","POST"])
def view():
    result = db.post.find().sort('timestamp',-1)
    return render_template("view.html", result = result, title = TITLE)
    
if __name__ == "__main__":
    app.run(debug = "True")
    
