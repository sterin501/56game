#!/usr/bin/python3

from flask import Flask, redirect, url_for, session , render_template , make_response,request
from datetime import datetime,timedelta
from authlib.integrations.flask_client import OAuth
from configparser import ConfigParser
import sqlite3

# decorator for routes that should be accessible only by logged in users
from auth_decorator import login_required





configur = ConfigParser()
configur.read('../config/config.ini')

app = Flask(__name__)
app.secret_key =configur.get('APP','APP_SECRET_KEY')
app.config['SESSION_COOKIE_NAME'] = 'google-login-session'
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=5)

# oAuth Setup
oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=configur.get('Google','client_id'),
    client_secret=configur.get('Google','client_secret'),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    access_token_params=None,
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    authorize_params=None,
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',  # This is only needed if using openId to fetch user info
    client_kwargs={'scope': 'openid email profile'},
)



@app.route('/')
def indexPage():
   now =  datetime.now()
   name=""
   #return render_template('lobby.html', name=name ,email=email)
   id = request.cookies.get('id')
   if  (id):
         return (render_template('index.html', name=name ,email=id))
   else:
         return (render_template('index.html', name=name ,email="not logged in"))



@app.route('/lobby')
@login_required
def hello_world():
   now =  datetime.now()
   name=""
   email=""
   id = request.cookies.get('id')
   #if  (id):
   #   name=searchforID(id)

   return render_template('lobby.html', name=name ,email=id)
   # res=make_response(render_template('lobby.html', name=name ,email=email))
   # res.set_cookie('id',id)
   # return res


@app.route('/table')              ## for secuirty we can add login_required later 
def mytable():
      id = request.cookies.get('id')
      if id:
         return render_template('56.html')
      return redirect('/login')



@app.route('/login')
def login():
       google = oauth.create_client('google')  # create the google oauth client
       redirect_uri = url_for('authorize', _external=True)
       return google.authorize_redirect(redirect_uri)


@app.route('/authorize')
def authorize():
       google = oauth.create_client('google')  # create the google oauth client
       token = google.authorize_access_token()  # Access token from google (needed to get user info)
       resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
       user_info = resp.json()
       user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
       # Here you use the profile/user data that you got and query your database find/register the user
       # and set ur own data in the session not the profile from google
       #print (user)
       print (user_info)
       session['profile'] = user_info
       session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
       #return redirect('/lobby')
       inserttoID(user_info['id'],user_info['email'].split("@")[0],user_info['name'])
       res=make_response( redirect('/lobby'))
       expire_date = datetime.now()
       expire_date = expire_date + timedelta(days=10)
       res.set_cookie('id',user_info['email'].split("@")[0],expires=expire_date)
       return res



@app.route('/logout')
def logout():
       for key in list(session.keys()):
           session.pop(key)
       return redirect('/')



def inserttoID(id,email,name):
    conn = sqlite3.connect('../config/mygame.db')
    conn.execute("INSERT OR IGNORE INTO ids (id,email,name) values ("+id+",'"+email+"','"+name+"');")
    conn.commit()
    print ("insert is fine ")
    conn.close()

def searchforID(id):
    conn = sqlite3.connect('../config/mygame.db')
    cursor = conn.execute("SELECT  email from ids where id="+id+";")
    email=cursor.fetchone()[0]
    #print(cursor.fetchone())
    conn.close()
    return email


##  CREATE TABLE  ids (id text UNIQUE, email text , name text );
## INSERT OR IGNORE INTO ids (id,email,name) values (111,'sgddg@gamil.com','sasi ');
