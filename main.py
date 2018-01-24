from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:12345@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

##
# TODO - Hash passwords.
##
# TODO - Do I need "before_request" handler and "require_login" function?
class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __init__(self, title, body, owner):
        self.title = title
        self.body = body
        self.owner = owner

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, username, password):
        self.username = username
        self.password = password

@app.route('/', methods=['POST', 'GET'])
def index():
    blog_titles = []
    bodys = []
    blogs = Blog.query.filter(Blog.id > 0).all()
    
    # TODO - Try doing this a more complex way, as the bonus suggests.
    #flip blogs list around, the simple way
    flipped_blogs = []
    for blog in reversed(blogs):
        flipped_blogs.append(blog)

    for blog in blogs:
        blog_titles.append(blog.title)
        bodys.append(blog.body)
    return render_template('blog.html',title="Build A Blog!", blogs=flipped_blogs, blog_titles=blog_titles, bodys=bodys)


@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    # TODO - Need validation to make sure body is string under 2000 characters, ad db.Column specifies above.

    # TODO - If either the blog title or blog body is left empty in the new post form, 
    #           the form is rendered again, with a helpful error message and 
    #           any previously-entered content in the same form inputs
    if request.method == 'POST':
        title = request.form['title']
        body = request.form['body']
        owner = User.query.filter_by(username=session['username']).first()
        if (title == '') or (body == ''): # TODO - come up with better validation tech.
            error = 'Please enter "Title" and "Content" for new blog entry...'
            return render_template('newpost.html', title="Build A Blog!", error=error) # TODO - rewrite this using Flash Messages.
        else:
            new_blog = Blog(title, body, owner)
            db.session.add(new_blog)
            db.session.commit()
            id = new_blog.id
            id = str(id)
            return redirect('/display?id='+id)
    return render_template('newpost.html', title="Build A Blog!")

@app.route('/display')
def display():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    blog_title = blog.title
    blog_body = blog.body
    return render_template('display.html', title="display blog here", blog_title=blog_title, blog_body=blog_body)

@app.route('/signup')

@app.route('/login', methods=["POST", "GET"])
def login():
    # TODO - add validation that makes sure username doesn't already exist and what-not.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username
            return redirct('/')
        elif user and user.password != password:
            return redirect('/login')# TODO - flash incorrect password.
        elif not user:
            return redirect('/login') # TODO - flash no user.

    return render_template('login.html')

@app.route('/index')

@app.route('/logout')
def logout():
    del session['username']
    return redirect('/')


if __name__ == '__main__':
    app.run()