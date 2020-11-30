import os
import json
from flask import Flask,render_template,url_for,flash,redirect
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)
app.config['SECRET_KEY'] = '374bef570b27058b66be0365a31a94c3'

# with open('../config.json','r') as c :
# 	params = json.load(c)["params"]


local_server = False
if local_server:
	app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://postgres:12aer56uil90@localhost/blogepedia"
else:
	app.config['SQLALCHEMY_DATABASE_URI'] = "postgres://myfothmmnpvigm:e4f604fb6e149b5bb5101eb1bfa7df175d6cdbd86e0be7d0c87b94cc13172003@ec2-54-175-77-250.compute-1.amazonaws.com:5432/d8qak2gjv1dqps"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

login_manager = LoginManager(app)

# this is for the @login_reuired decorartor to understand to take to the login sceen if the user is not logged in and trying to access the accounts screen ,, after = wwe put the funtion name
login_manager.login_view = 'users.login'
# inorder to make our message of access dined in format of flsh meszage
login_manager.login_message_category = 'info'
