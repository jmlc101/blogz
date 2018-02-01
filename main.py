from flask import Flask, request, redirect, render_template, session, flash
from models import validate_input, User, Blog
from app import app, db

from hashutils import check_pw_hash
# TODO - Testing branch protection configurations.
# TODO - add Pagination "bonus mission"
# TODO - Hash passwords. "bonus mission"
# TODO - Try to break it.
# TODO - Implement an auto log out function.
# TODO - Lets add some cookies.


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
            flipped_blogs = []
            for blog in reversed(blogs):# TODO - Try doing this a more complex way, as the bonus suggests.
                flipped_blogs.append(blog)
            return render_template('singleUser.html', user=user, blogs=flipped_blogs)
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
            return redirect('/blog?id='+id)
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
            return validate_input(username, password, verify, email) #I hate this validation style.
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
        if user and check_pw_hash(password, user.pw_hash):
            session['username'] = username 
            flash("Welcome! You're Logged in!")
            # test
            
            ##########################
            # test complete
            return redirect('/newpost')
        elif user and user.password != password:### need to insert user into template so they dont have to retype.
            flash('Incorrect password.')
            return redirect('/login')
        elif not user:
            flash('Username does not exist.')
            return redirect('/login')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    flash("Logged Out.")
    return redirect('/blog')

if __name__ == '__main__':
    app.run()