import os
import sqlite3
from flask import Flask,render_template, request, redirect,session

app = Flask(__name__, instance_path=os.path.abspath(__file__))
app.secret_key='yaogeandmingbozhang' #set the key for login

@app.route('/',methods=['GET','POST'])
def welcome():
    if request.method == 'GET':
        return render_template('welcome.html') 
    user = request.form.get('user') #get the username 
    pwd = request.form.get('pwd') #get the password
    if user == 'user' and pwd =="password":
        session['user_info'] = user #save user info to session
        return redirect("/index") # jump to index if correct input
    else:
        return render_template('welcome.html',msg = 'wrong user or password')

@app.route('/index')
def index():
    user_info = session.get('user_info')
    if not user_info:
        return redirect('/welcome')
    return render_template('index.html')

@app.route('/logout')
def logout():
    del session['user_info']
    return redirect('/welcome')

if __name__ == '__main__':
    app.run()