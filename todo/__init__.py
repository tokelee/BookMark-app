import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_moment import Moment
from flask_mail import Mail
from flask_debugtoolbar import DebugToolbarExtension

app=Flask(__name__)

moment = Moment(app)

app.config['SECRET_KEY']='\x00\xe9\xab\xe7n\xb9\x03.0\xa3\xae\x92\x10>\xbf\x7f\x16\x8b;X9\xf1\xfd\xd2\x88\x97\xfa\x993j'
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:tokelee@localhost:3306/todo'
app.config['SQLALCHEMY_ECHO']=True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False
app.config['DEBUG_TB_INTERCEPT_REDIRECTS']=False
app.debug = True
#mail--configuration
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_USERNAME'] = os.environ.get('MAIL_PASSWORD')


db=SQLAlchemy(app)
mail = Mail(app)
toolbar=DebugToolbarExtension(app)


login_manager=LoginManager()
login_manager.init_app(app)
login_manager.login_view='login'

from todo import route