def validate_input(username, password, verify, email):
    from flask import Flask, render_template, request, redirect, flash
    import re
    from sign_up_validation import SignUpValidation
    
    from main import db, User # Keep an eye on this stuff.

    from flask import session # is this proper use of sessions?

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
    
    if tom.valid:
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
            flash("Welcome! You're Logged in!")
            return redirect("newpost.html")
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