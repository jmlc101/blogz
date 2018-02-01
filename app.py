from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_sslify import SSLify

app = Flask(__name__)

sslify = SSLify(app)

app.config['DEBUG'] = True
# Note: the connection string after :// contains the following info:
# user:password@server:portNumber/databaseName
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://blogz:12345@localhost:8889/blogz'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)
app.secret_key = 'PublicTestKey' # TODO - Made Public! Change this for private app! :)