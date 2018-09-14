from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_sslify import SSLify

app = Flask(__name__)

sslify = SSLify(app)

# TODO - Change DEBUG to False in order for the flask-sslify extenion to work. Redirects incoming requests to Https.
# obviously, change to True to see DEBUG in Terminal when running app.
app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://Blogz:Blogz@localhost:3306/Blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'PublicTestKey' # TODO - Made Public! Change this for private app! :)