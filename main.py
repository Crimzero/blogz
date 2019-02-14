from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
import cgi
import os
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:blogz@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Muffins'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.column(db.Integer, foreign_key=User.id)
    title = db.Column(db.String(120))
    content = db.Column(db.String(240))
    def __init__(self, owner_id, title, content):
        self.owner_id = owner_id
        self.title = title
        self.content = content

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(120))
    #blogs = db.relationship('Blog', backref ='owner')
    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password

#Password confimation function
def confirm(pwd, confirm_pwd):
    if pwd == confirm_pwd:
        return True
    else:
        return False

#Email validation function
def isValidEmail(email):
        if len(email) > 3 and len(email) < 21:
            if re.match("^.*?@.*?\.[a-z]{2,}?$", email) != None:
                return True
        return False
    
@app.before_request
def require_login():
    allowed_routes = ['login', 'signup']
    if request.endpoint not in allowed_routes and 'email' not in session:
        return redirect('/signup')

@app.route('/', methods=['POST', "GET"])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', title='BLOGZ', blogs=blogs)

@app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        pwd = request.form['pwd']
        confirm_pwd = request.form['confirm_pwd']
        username_blank_error = ''
        username_length_error = ''
        username_space_error = ''
        email_invalid_error = ''
        pwd_blank_error = ''
        pwd_requirement_error = ''
        confirm_pwd_blank_error = ''
        confirm_error = ''
    existing_user = User.query.filter_by(email=email).first()

#Username    
    if username == '':
        username_blank_error = '*Required field'
    elif ' ' in username:
        username_space_error = "You can't put a space in your user name.  Come on man, get it together...'"
    else:
        if len(username) < 3 or len(username)> 20:
            username_length_error = 'Username must be between 3 and 20 characters'
#Email
    if email == '':
        pass 
    elif isValidEmail(email) == False :
        email_invalid_error = 'This email is invalid, try again.'
#Pwd
    if confirm_pwd == '':
        confirm_pwd_blank_error = '*Required field' 
    if pwd == '':
        pwd_blank_error = '*Required field'
    elif len(pwd) < 3 or len(pwd)> 20:
        pwd_requirement_error = 'Password must be between 3 and 20 characters'
    elif not confirm(pwd, confirm_pwd):
        confirm_error = 'You screwed up confirming your password, try again.'
        pwd = ''
        confirm_pwd = ''
#Render
    if  username_blank_error or username_length_error or username_space_error or email_invalid_error or pwd_blank_error or pwd_requirement_error or confirm_pwd_blank_error or confirm_error:
        return render_template('signup.html', title='Blogz Sign-up', username=username, email=email, pwd='', confirm_pwd='', username_blank_error=username_blank_error, username_length_error=username_length_error, username_space_error=username_space_error, email_invalid_error=email_invalid_error, pwd_blank_error=pwd_blank_error, pwd_requirement_error=pwd_requirement_error, confirm_pwd_blank_error=confirm_pwd_blank_error, confirm_error=confirm_error)
    elif not existing_user:
        new_user = User(username, email, pwd)
        db.session.add(new_user)
        db.session.commit()
        session['email'] = email
        return redirect('/')
    else:
        # response msg
        return '<h1>Duplicate user</h1>'
    
@app.route('/login', methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['pwd']
        user = User.query.filter_by(email=email).first()
        if user and user.password == password:
            session['email'] = email
            flash('Logged in')
            print(session)
            return redirect('/')
        else:
            flash('User passwrod blah blah blah', 'error')
    return render_template('login.html')

@app.route('/blog')
def blog():    
    blogs = Blog.query.all()
    return render_template('blog.html', title='The BLOG', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('/newpost.html')
        
    if request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        if title == '':
            flash('*Title is required', 'error')
            return render_template('/newpost.html', title=title, content=content)
        if content == '':
            flash('*Content is required', 'error')
            return render_template('/newpost.html', title=title, content=content)
        elif len(content) > 240:
            flash('*Too verbose, get to the point', 'error')
            return render_template('/newpost.html', title=title, content=content)

        new_blog = Blog(title, content)
        
        db.session.add(new_blog)
        db.session.commit()
        return render_template('/single_blog.html', title=new_blog.title, content=new_blog.content, blog=new_blog )

@app.route('/single_blog', methods=['GET'])

def display_blog():
    blog_id = request.args.get('id')
    blog = Blog.query.get(blog_id)
    return render_template('/single_blog.html', title=blog.title, content=blog.content, blog=blog)


if __name__ == "__main__":
    app.run()