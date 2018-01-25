from flask import Flask, request, redirect, render_template, session, flash
from flask_sqlalchemy import SQLAlchemy
from validate_input import validate_input
from datetime import datetime


app = Flask(__name__)
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:12345@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'IllWorryAboutThisLater' # TODO - worry about this :)

# TODO - Need to change '/' to '/blog' and '/home' to '/' as per directions....
##
# TODO - Hash passwords.
# TODO - Try to break it.


class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(120))
    body = db.Column(db.String(2000))
    owner_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    pub_date = db.Column(db.DateTime)


    def __init__(self, title, body, owner, pub_date=None):
        self.title = title
        self.body = body
        self.owner = owner
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date

    def __repr__(self):
        return str(self.owner)

class User(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(120))
    password = db.Column(db.String(120))
    email = db.Column(db.String(120))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, username, password, email):
        self.username = username
        self.password = password
        self.email = email

@app.before_request
def require_login():
    allowed_routes = ['login', 'list_blogs', 'index', 'signup', 'logout']
    if request.endpoint not in allowed_routes and 'username' not in session:
        flash("Please Log In to post blog's")
        return redirect('/login')

@app.route('/') # TODO - Change this to '/'
def index():
    users = User.query.filter(User.id > 0).all()
    return render_template('index.html', users=users)

@app.route('/blog', methods=['POST', 'GET'])
def list_blogs():
    
    if request.method == 'GET':
        userID = request.args.get('user')
        blogID = request.args.get('id')
        if userID:
            user = User.query.filter_by(id=userID).first()
            blogs = Blog.query.filter_by(owner=user).all()
            return render_template('singleUser.html', user=user, blogs=blogs)
        elif blogID:
            blog = Blog.query.filter_by(id=blogID).first()
            return render_template('display.html', title="display blog here", blog=blog)
        else:
            bodys = []
            blogs = Blog.query.filter(Blog.id > 0).all()
            flipped_blogs = []
            for blog in reversed(blogs):# TODO - Try doing this a more complex way, as the bonus suggests.
                flipped_blogs.append(blog)

            for blog in blogs:
                bodys.append(blog.body)
            return render_template('blog.html', title="Blogs", blogs=flipped_blogs, bodys=bodys)

# Dead code beneath?:
#    blog_titles = [] # Dead Code?
#    bodys = []
#    blogs = Blog.query.filter(Blog.id > 0).all()
#    
#    # TODO - Try doing this a more complex way, as the bonus suggests.
#    #flip blogs list around, the simple way
#    flipped_blogs = []
#    for blog in reversed(blogs):
#        flipped_blogs.append(blog)###
#
#    for blog in blogs:
#        blog_titles.append(blog.title) # Dead Code?
#        bodys.append(blog.body)
#    return render_template('blog.html',title="Build A Blog!", blogs=flipped_blogs, blog_titles=blog_titles, bodys=bodys)

@app.route('/singleUser')
def users_blogs():
    id = request.args.get('id')
    user = User.query.filter_by(id=id).first()
    blogs = Blog.query.filter_by(owner=user).all()
    return render_template('singleUser.html', user=user, blogs=blogs)

@app.route('/display')
def display():
    id = request.args.get('id')
    blog = Blog.query.filter_by(id=id).first()
    blog_title = blog.title
    blog_body = blog.body
    return render_template('display.html', title="display blog here", blog_title=blog_title, blog_body=blog_body, blog=blog)

@app.route('/newpost', methods=['POST', 'GET'])
def newpost():
    # TODO - Need validation to make sure body is string under 2000 characters, as db.Column specifies above.

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





@app.route('/signup', methods=['POST', 'GET'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        verify = request.form['verify']
        email = request.form['email']

        existing_user = User.query.filter_by(username=username).first() #If user exists, will assign vaule, otherwise will assign 'NONE'.
        if not existing_user:
            return validate_input(username, password, verify, email)
        else:
            return render_template('signup.html', user_name_error='Username already exists.')

    return render_template('signup.html')

@app.route('/login', methods=["POST", "GET"])
def login():
    if 'username' in session:
        flash('Already logged in.')
        return redirect('/blog')
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        user = User.query.filter_by(username=username).first()
        if user and user.password == password:
            session['username'] = username 
            flash("Welcome! You're Logged in!")
            return redirect('/newpost')
        elif user and user.password != password:
            flash('Incorrect password.')
            return redirect('/login')
        elif not user:
            flash('Username does not exist.')
            return redirect('/login')

    return render_template('login.html')

@app.route('/index')

@app.route('/logout')
def logout():
    if 'username' in session:
        del session['username']
        flash("You've logged out.")
        return redirect('/blog')
    elif 'username' not in session:
        flash("Not logged in.")
        return redirect('/blog')

if __name__ == '__main__':
    app.run()