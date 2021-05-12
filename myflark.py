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

# 定义ORM
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

        
# 创建表格、插入数据
def create_db():
    db.drop_all()  # 每次运行，先删除再创建
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


# 登录检验（用户名、密码验证）
def valid_login(username, password):
    user = User.query.filter(and_(User.username == username, User.password == password)).first()
    if user:
        return True
    else:
        return False


# 注册检验（用户名、邮箱验证）
def valid_regist(username, email):
    user = User.query.filter(or_(User.username == username, User.email == email)).first()
    if user:
        return False
    else:
        return True


# 主页
@app.route('/')
def home():
    return render_template('welcome.html', username=session.get('username'))

## 注册
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
#登录
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

#主页
@app.route('/index')
def index():
    user_info = session.get('username')
    if not user_info:
        return redirect('/')

    return render_template('index.html')   

# 注销
@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('home'))

# 个人中心
@app.route('/panel')
def panel():
    username = session.get('username')
    if not username:
        return redirect('/')
    
    #返回的是列表
    user = User.query.filter(User.username == username).first()
    favor= db.session.query(Favor).filter(Favor.username == username).all()
    
    return render_template("panel.html", user=user,favor=favor)


#试题1
@app.route('/page1', methods=['GET', 'POST'])
def page1():
    MSG = None
    username = session.get('username')
    if not username:
        return redirect('/')
    #收藏功能
    user = User.query.filter(User.username == username).first()
    favor= db.session.query(Favor).filter(Favor.username == username).all()
    #如果没有收藏，那么添加搜藏，如果有添加，显示已经添加

    if request.method == 'POST':
        page="page1"
        temp=[]
        for i in range(len(favor)):
            b=favor[i].favorite
            temp.append(b)
        if page in temp:
        #已经搜藏显示
            MSG='Already add to Favor'
        else:
            fav = Favor(username=user.username, favorite=page)
            fav.us=user
            db.session.add(fav)
            db.session.commit()
            MSG='Successful adding'

    return render_template("page1.html",MSG=MSG)

if __name__ == '__main__':
    app.run(debug=True)
