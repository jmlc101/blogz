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
        if re.search(email_regex, email):
            self.validation_count += 6
            return True
        elif re.search(email_regex, email) == None:
            return False

    def valid_count(self):
        if (self.validation_count == 5) or (self.validation_count == 11):
            self.valid = True
        return self.validation_count

    def __repr__(self):
        return str(self.valid) 