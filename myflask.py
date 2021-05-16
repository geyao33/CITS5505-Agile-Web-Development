# flask_sqlalchemy.py
import os
import sqlite3
from flask import Flask, request, render_template, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import and_, or_, ForeignKey
from sqlalchemy.orm import relationship

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.secret_key='yaogeandmingbozhang' #set the key for login
db = SQLAlchemy(app)

# ORM
class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(80))
    email = db.Column(db.String(120), unique=True)
    
    fav=db.relationship('Favor',backref='User',lazy='dynamic')

    def __repr__(self):
        return '<User %r>' % self.username

class Favor(db.Model):
    __tablename__ = 'favor'

    num = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80))
    id = db.Column(db.Integer, db.ForeignKey('users.id'))
    favorite = db.Column(db.String(120))

    us=db.relationship('User',backref='favor')

    def __repr__(self):
        return '<Favor %r>' % self.favorite

        
# DB and tables
def create_db():
    db.drop_all()  # delete and create new DB when start
    db.create_all()
    
    admin = User(username='admin', password='root', email='admin@example.com')
    db.session.add(admin)

    user1=User(username='guest1', password='guest1', email='guest1@example.com')
    user2=User(username='guest2', password='guest2', email='guest2@example.com')

    favor1 = Favor(username='guest1', favorite="page1")
    favor2 = Favor(username='guest1', favorite="page2")

    favor1.us=user1
    favor2.us=user1

    db.session.add_all([favor1, favor2])
    db.session.add_all([user1, user2])
    db.session.commit()

create_db()


# check the login
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False


# check the registration
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True


# welcome page
@app.route('/')
def home():
    return render_template('welcome.html', username=session.get('username'))

## regist
@app.route('/regist', methods=['GET','POST'])
def regist():
    error = None
    if request.method == 'POST':
        if request.form['password1'] != request.form['password2']:
            error = 'different input！'
        elif valid_regist(request.form['username'], request.form['email']):
            user = User(username=request.form['username'], password=request.form['password1'], email=request.form['email'])
            db.session.add(user)
            db.session.commit()
            
            flash("Successful registration！")
            return redirect(url_for('login'))
        else:
            error = 'username or email had been used！'
    
    return render_template('regist.html', error=error)

#login
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if valid_login(request.form['username'], request.form['password']):
            flash("Successful login！")
            session['username'] = request.form.get('username')
            return redirect(url_for('index'))
        else:
            error = 'wrong passward or username！'

    return render_template('login.html', error=error)

#index
@app.route('/index', methods=['GET', 'POST'])
def index():
    user_info = session.get('username')
    if not user_info:
        return redirect('/')
    page1="page1"
    page2="page2"

    return render_template('index.html',page1=page1,page2=page2)   

#logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

#account panel
@app.route('/panel')
def panel():
    username = session.get('username')
    if not username:
        return redirect('/')
    
    #the query return a list
    user = User.query.filter(User.username == username).first()
    favor= db.session.query(Favor).filter(Favor.username == username).all()
    
    return render_template("panel.html", user=user,favor=favor)


#test page
@app.route('/test/<numberpage>', methods=['GET', 'POST'])
def test(numberpage):
    pagefile= numberpage+'.html'
    MSG = None
    username = session.get('username')
    if not username:
        return redirect('/')
    #add to favor funtion
    user = User.query.filter(User.username == username).first()
    favor= db.session.query(Favor).filter(Favor.username == username).all()
    #if added then drop, if havent added then add

    if request.method == 'POST':
        page=numberpage
        temp=[]
        for i in range(len(favor)):
            b=favor[i].favorite
            temp.append(b)
        if page in temp:
            fav = db.session.query(Favor).filter(and_(Favor.username == user.username, Favor.favorite == page)).first()
            db.session.delete(fav)
            db.session.commit()
            MSG='Successful dropping'
        else:
            fav = Favor(username=user.username, favorite=page)
            fav.us=user
            db.session.add(fav)
            db.session.commit()
            MSG='Successful adding'
 
    return render_template(pagefile,MSG=MSG)
    

if __name__ == '__main__':
    app.run(debug=True)
