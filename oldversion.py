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

user = User.query.filter(User.username == 'guest1').first()
a=db.session.query(Favor).filter(Favor.username == 'guest1').all()

page="page1"
C=[]
for i in range(len(a)):
    b=a[i].favorite
    C.append(b)

if page in C:
    print("yes")

print(user)
temp = db.session.query(Favor).filter(and_(Favor.username == 'guest1', Favor.favorite == "page1")).first()
print(a)
print(temp)
db.session.delete(temp)
db.session.commit()
print(db.session.query(Favor).filter(Favor.username == 'guest1').all())