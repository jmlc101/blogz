from flask import Flask, render_template, request, redirect, flash, session
from app import db
from datetime import datetime
import re

from hashutils import make_pw_hash

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
    pw_hash = db.Column(db.String(120))
    email = db.Column(db.String(120))
    blogz = db.relationship('Blog', backref='owner')

    def __init__(self, username, password, email):
        self.username = username
        self.pw_hash = make_pw_hash(password)
        self.email = email

class SignUpValidation:
    import re 
    regex = re.compile(r"\w{3,20}")
    def __init__(self):
        self.validation_count = 0
        self.valid = False
        
    def validate_username(self, username):
        import re
        regex = re.compile(r"\w{3,20}")
        if regex.search(username):
            self.validation_count += 1
            return True
        elif regex.search(username) == None:
            return False

    def validate_password(self, password):
        import re
        regex = re.compile(r"\w{3,20}")
        if regex.search(password):
            self.validation_count += 1
            return True
        elif regex.search(password) == None:
            return False
        

    def validate_pass_verify(self, password, verify):
        import re
        regex = re.compile(r"\w{3,20}")
        if (password == verify) and regex.search(password):
            self.validation_count += 3
        if (password == verify):
            return True
        else:
            return False
        
    def validate_email(self, email):
        import re
        email_regex = r"^\w+@\w+\.\w+$"
        if email == '':
            self.validation_count += 6
            return True
        elif re.search(email_regex, email):
            self.validation_count += 6
            return True
        elif re.search(email_regex, email) == None:
            self.validation_count += 1
            return False

    def valid_count(self):
        if (self.validation_count == 5) or (self.validation_count == 11):
            self.valid = True
        return self.validation_count

    def __repr__(self):
        return str(self.valid) 


def validate_input(username, password, verify, email):

    name_error_msg = "That's not a valid username"
    pass_error_msg = "That's not a valid password"
    nonmatch_error = "Passwords don't match"
    email_err = "That's not a valid email address"
    
    tom = SignUpValidation()
    tom.validate_username(username)
    tom.validate_password(password)
    tom.validate_pass_verify(password, verify)
    tom.validate_email(email)
    tom.valid_count()
    
    if tom.valid == True:
        new_user = User(username, password, email)
        db.session.add(new_user)
        db.session.commit()
        session['username'] = username 
        flash("Welcome! You're Logged in!")
        return redirect("/newpost")
        
    if username == '':
        if password == '':
            if verify != '':
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email=email)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email_error=email_err)
            elif verify == '':
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email=email)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email_error=email_err)
        else:
            if tom.validate_password(password):
                if password == verify:
                    if tom.validate_email(email) or (email == ''):
                        return render_template("signup.html", user_name_error=name_error_msg, email=email)
                    else:
                        return render_template("signup.html", user_name_error=name_error_msg, email_error=email_err)
                else:
                    if tom.validate_email(email) or (email == ''):
                        return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email=email)
                    else:
                        return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email_error=email_err)
            else:
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email=email)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email_error=email_err)

    if password == '':
        if tom.validate_username(username):
            if tom.validate_email(email) or (email == ''):
                return render_template("signup.html", name=username, pass_error=pass_error_msg, email=email)
            else:
                return render_template("signup.html", name=username, pass_error=pass_error_msg, email_error=email_err)
        else:
            if tom.validate_email(email) or (email == ''):
                return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email=email)
            else:
                return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email_error=email_err)

    if verify == '':
        if tom.validate_username(username):
            if tom.validate_password(password):
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", name=username, verify_pass_error=nonmatch_error, email=email)
                else:
                    return render_template("signup.html", name=username, verify_pass_error=nonmatch_error, email_error=email_err)
            else:
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", name=username, pass_error=pass_error_msg, email=email)
                else:
                    return render_template("signup.html", name=username, pass_error=pass_error_msg, email_error=email_err)
        else:
            if tom.validate_password(password):
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email=email)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, verify_pass_error=nonmatch_error, email_error=email_err)
            else:
                if tom.validate_email(email) or (email == ''):
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email=email)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email_error=email_err)


    regex = re.compile(r"\w{3,20}")
    regex2 = r"([\w\W]+) ([\w\W]+)"
    regex3 = r"([\w\W]+) ([\w\W]+) ([\w\W]+)"
    email_regex = r"^\w+@\w+\.\w+$"
    
    tple = username, password, verify
    string = ' '.join(tple)
    tple2 = username, password
    string2 = ' '.join(tple2)
    grps = re.search(regex3, string)
    grps2 = re.search(regex2, string2)

    if regex.search(grps.group(1)) and regex.search(grps.group(2)) and (password == verify):
        if (regex.search(email) and re.search(email_regex, email)) or (email == ''):
            new_user = User(username, password, email)
            db.session.add(new_user)
            db.session.commit()
            session['username'] = username
            flash("Welcome! You're Logged in!") # is this Dead code?????????????/
            return redirect("/newpost")
        else:
            return render_template("signup.html", email_error=email_err, name=username)
    elif regex.search(grps2.group(1)) and regex.search(grps2.group(2)):
        if (regex.search(email) and re.search(email_regex, email)) or (email == ''):
            return render_template("signup.html", email=email, name=username, verify_pass_error=nonmatch_error)
        else:
            return render_template("signup.html", name=username, verify_pass_error=nonmatch_error, email_error=email_err)
    elif re.search(regex, username):
        if (regex.search(email) and re.search(email_regex, email)) or (email == ''):
            return render_template("signup.html", email=email, name=username, pass_error=pass_error_msg)
        else:
            return render_template("signup.html", name=username, pass_error=pass_error_msg, email_error=email_err)
    else:
        if (regex.search(email) and re.search(email_regex, email)) or (email == ''):
            if regex.search(password):
                if password == verify:
                    return render_template("signup.html", email=email, user_name_error=name_error_msg)
                else:
                    return render_template("signup.html", email=email, user_name_error=name_error_msg, verify_pass_error=nonmatch_error)
            else:
                return render_template("signup.html", email=email, user_name_error=name_error_msg, pass_error=pass_error_msg)
        else:
            if regex.search(password):
                if password == verify:
                    return render_template("signup.html", user_name_error=name_error_msg, email_error=email_err)
                else:
                    return render_template("signup.html", user_name_error=name_error_msg, email_error=email_err, verify_pass_error=nonmatch_error)
            else:
                return render_template("signup.html", user_name_error=name_error_msg, pass_error=pass_error_msg, email_error=email_err)