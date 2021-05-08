import os
import sqlite3
from flask import Flask,render_template, request, redirect

app = Flask(__name__, instance_path=os.path.abspath(__file__))

@app.route('/',methods=['GET','POST'])
def welcome():
    if request.method == 'GET':
        return render_template('welcome.html') 
    user = request.form.get('user') #get the username 
    pwd = request.form.get('pwd') #get the password
    if user == 'user' and pwd =="password":
        return redirect("/index") # jump to index if correct input
    else:
        return render_template('welcome.html',msg = 'wrong user or password')

@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()