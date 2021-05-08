import os
import sqlite3
from flask import Flask,render_template

app = Flask(__name__, instance_path=os.path.abspath(__file__))

@app.route('/',methods=['GET','POST'])
def welcome():
    return render_template('welcome.html')


@app.route('/index')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run()