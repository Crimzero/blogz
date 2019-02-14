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
        self.title = title
        self.content = content

@app.route('/', methods=['POST', "GET"])
def index():
    blogs = Blog.query.all()
    return render_template('blog.html', title='The BLOG', blogs=blogs)

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