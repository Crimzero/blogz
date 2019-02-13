from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:build-a-blog@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'Muffins'

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    content = db.Column(db.String(240))
    def __init__(self, title, content):
        #self.id = id
        self.title = title
        self.content = content

@app.route('/', methods=['POST', "GET"])
def index():

    #if request.method == 'POST':
     #   title = request.form['title']
      #  content = request.form['content']
       # new_blog = Blog(title, content)
        #db.session.add(new_blog)
        #db.session.commit()
    blogs = Blog.query.all()
    return render_template('blog.html', title='The BLOG', blogs=blogs)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    if request.method == 'GET':
        return render_template('/newpost.html', title='The BLOG')
        
    elif request.method == 'POST':
        title = request.form['title']
        content = request.form['content']
        new_blog = Blog(title, content)
        db.session.add(new_blog)
        db.session.commit()
        return redirect('/')
if __name__ == "__main__":
    app.run()